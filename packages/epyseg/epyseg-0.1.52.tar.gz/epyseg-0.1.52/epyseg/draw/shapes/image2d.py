# I guess there is a big bug in the scales of the components --> hack this
from epyseg.pyqt.tools import check_antialiasing
# TODO --> rename position into placement

# faire un draw_at_scale and merge draw fill etc by just putting an option --> much simpler and that way you can keep original size which is the best idea
# set to width doit juste calculer le scaling factor in fact.... --> TODO do that and same for all objects --> no cloning and all will be simpler

# check all the things that need be packed top left/top right/bottom left/bottom right
# letter should always be packed first and top left
# make insets, etc more flexible
# should I remove the letter of insets ???
# the rest can be any position and any nb of instances of text/scale bar or insets
# see how to edit that easily
# TODO
# objects can be scale bars and or insets and or text labels as many as needed --> pack them in x or y and align them

# https://docs.python.org/2/library/operator.html
# maths fig in inkscape --> cool using latex https://castel.dev/post/lecture-notes-2/

# TODO may also contain svg or graphs or ???
# TODO handle extra labels for images directly and also for rows or cols --> think how to do that but must be doable

# TODO Add the crops --> see how though and see how to warn when width or height reaches 0...
# should I offer max projections too ??? maybe or not --> see how to do that...

# the only advantage I see for rect2D vs qrectf is that they allow for rotation ????
# see how to best handle that ???

from epyseg.settings.global_settings import set_UI # set the UI to be used py qtpy
set_UI()
from epyseg.serialization.tools import create_objects_from_dict, object_to_xml
from epyseg.matplolib.tools import get_fig_rect
import os
import traceback
from epyseg.draw.shapes.Position import groupby_position, Position
from epyseg.draw.shapes.rectangle2d import Rectangle2D
import numpy as np
import matplotlib.pyplot as plt
from qtpy import QtGui
from qtpy.QtGui import QPainter, QColor, QBrush, QPen, QTransform, QFontMetrics
from qtpy.QtCore import Qt
from qtpy.QtSvg import QSvgGenerator
from qtpy.QtSvg import QSvgRenderer
from epyseg.draw.shapes.line2d import Line2D
from epyseg.draw.shapes.point2d import Point2D
from epyseg.figure.alignment import alignRight, alignLeft, alignTop, alignBottom, alignCenterH, alignCenterV, packY, \
    packX, packYreverse, pack2, packing_modes
from epyseg.draw.shapes.scalebar import ScaleBar
from epyseg.draw.shapes.txt2d import TAText2D
from epyseg.figure.fig_tools import preview
# from epyseg.figure import fig_tools
from epyseg.img import Img, toQimage, RGB_to_BGR
from qtpy.QtCore import QRectF, QPointF, QSize, QRect
from qtpy.QtWidgets import QApplication
import sys
import io
from epyseg.tools.logger import TA_logger

logger = TA_logger()

class Image2D(Rectangle2D):

    def __init__(self, *args, x=None, y=None, width=None, height=None, data=None, dimensions=None, filename=None, isText=False, fraction_of_parent_image_width_if_image_is_inset=0.25, opacity=1., theta=None, crop_left=0, crop_right=0, crop_top=0, crop_bottom=0,fill_color=None, border_color=0xFFFFFF,border_size=None, placement=Position('Top-Right'),annotations=None, custom_loading_script=None, allow_unknown_files=True, scale=1, **kwargs):

        if kwargs:
            print('ignored parameters', kwargs)
        # Image2D._count += 1
        # self.ID = Image2D._count
        # print(**kwargs)

        # if this stuff is set then allow to load the image using that -−> TODO

        self.custom_loading_script = custom_loading_script # TODO implement that --> should assign to self.img smthg that I can handle -−> either a raster or a svg or whatever # par exemple pr loader les certains frames d'une image -−> qq chose de facile à faire
        # self.custom_post_loading_script = custom_post_loading_script

        # crops
        self.crop_left = crop_left
        self.crop_right = crop_right
        self.crop_top = crop_top
        self.crop_bottom = crop_bottom
        self.img = None
        self.line_style = None # useless yet just for compat
        if not annotations: # DEV NOTE KEEP WEIRD SERIALIZATION CODE IF I DONT DO THAT --> SO KEEP --> IF I INITITATE annotations = [] in the init then nested images in annotations cause an infinite loop in serialization, no clue why though
            annotations = []
        # if annots is a dict --> try to rebuild all the objects maybe

        # print('TADA', type(annotations), len(annotations))

        if isinstance(annotations, dict):
            # print('this is a fucking dict')
            annotations=create_objects_from_dict(annotations) # it is really there but this can really contain many... --> need a fix
        # elif isinstance(annotations, str):

        self.annotations=annotations
        if isinstance(placement, str):
            placement = Position(placement)
        self.placement=placement
        self.renderer = None # replaced all of these by self.img
        # self.annotation = []  # should contain the objects for annotating imaging --> shapes and texts
        # self.letter = None  # when objects are swapped need change the letter
        # self.top_left_objects = []
        # self.top_right_objects = []
        # self.bottom_right_objects = []
        # self.bottom_left_objects = []
        # self.centered_objects = []

        # if the image is inserted as an inset then draw it as a fraction of parent width
        # inset parameters
        self.fraction_of_parent_image_width_if_image_is_inset = fraction_of_parent_image_width_if_image_is_inset
        self.border_size = border_size  # no border by default
        self.border_color = border_color  # white border by default
        self.filename = filename

        if not args and filename:
            args = [filename]

        if args:
            # if len(args) == 1:
                if isinstance(args[0], str):
                    self.filename = args[0]
                elif isinstance(args[0], Img):
                    self.filename = None
                    self.img = args[0]
                    self.qimage = toQimage(self.img)
                    if x is None:
                        x = 0
                    if y is None:
                        y = 0
                    try:
                        super(Image2D, self).__init__(x, y, self.img.get_width(), self.img.get_height())
                    except:
                        super(Image2D, self).__init__(x, y, self.img.shape[1], self.img.shape[0])
                elif isinstance(args[0], plt.Figure):
                    # the passed image is in fact a matplotlib plot --> init super with the corresponding QrectF
                    super(Image2D, self).__init__(get_fig_rect(args[0]))
                    self.img = args[0]
                    self.setFigure(self.img)
                # elif isinstance(args[0], TAText2D):
                #     self.img = args[0]
                #     self.filename = args[0]
                #     super(Image2D, self).__init__(args[0].getRect(all=True))
        # else:
        #     self.filename = filename

        if x is None and y is None and width is not None and height is not None and self.filename is None:
            super(Image2D, self).__init__(0, 0, width, height)
        elif self.filename is not None: # and not isinstance(self.filename, TAText2D):
            # handle svg files first
            if self.filename.lower().endswith('.svg'):
                # print('loading svg here!!!')
                # create empty rect then

                super(Image2D, self).__init__(0, 0, 512, 512) # fake definition
                self.setFigure(self.filename) #real loading of the parameters
            else:
                # print('in 0')
                try:
                    self.img = Img(self.filename)
                    # try squeeze it ??? --> maybe not --> but I need make sure the image is channel last
                    # print(self.img.dtype, self.img.shape)
                    self.qimage = toQimage(self.img)
                    width = self.qimage.width()
                    height = self.qimage.height()

                    # print('width, height',width, height)

                    # if width is None:
                    #     width = self.img.shape[1]
                    # if height is None:
                    #     height =self.img.shape[0]

                    super(Image2D, self).__init__(0, 0, width, height)
                except:
                    logger.error('could not load image '+str(self.filename))

                    if not allow_unknown_files:
                        return
                    else:
                        # define a default image with 512x512 and display error on top of it
                        # in fact this can be an empty image
                        self.img = None # this is the indication that an error occurred and that I cannot do much
                        super(Image2D, self).__init__(0, 0, 512, 512)
            if x is not None:
                self.setX(x)
            if y is not None:
                self.setY(y)
            if width is not None:
                self.setWidth(width)
            if height is not None:
                self.setHeight(height)


        elif x is not None and y is not None and width is not None and height is not None and self.img is None:
            self.img = None
            super(Image2D, self).__init__(x, y, width, height)
        elif self.filename is not None: # and not isinstance(self.filename, TAText2D):
                self.img = Img(self.filename)
                self.qimage =  toQimage(self.img)
                if x is None:
                    x = 0
                if y is None:
                    y = 0
                super(Image2D, self).__init__(x, y, self.img.get_width(), self.img.get_height())
        # elif data is not None:
        #     self.img = Img(data,
        #                    dimensions=dimensions)  # need width and height so cannot really be only a numpy stuff --> cause no width or height by default --> or need tags such as image type for dimensions
        #     self.qimage =  toQimage(self.img)
        #     # need Image dimensions id data is not of type IMG --> could check that
        #     if x is None:
        #         x = 0
        #     if y is None:
        #         y = 0
        #     super(Image2D, self).__init__(x, y, self.img.get_width(), self.img.get_height())

        # TODO keep it here otherwise it is reset by super or pass it as a parameter to super --> ideally I should always call super first but here I can't
        self.opacity = 1
        self.scale = scale
        self.translation = QPointF()
        self.fill_color = fill_color  # can be used to define a bg color for rotated images (and or transparent images...)
        self.theta=theta
        self.isText = isText
        # self.fill_color = 0xFF0000  # can be used to define a bg color for rotated images (and or transparent images...)

        # self.check_if_image2d_init_called()

        # run the script at the very end but maybe need to do things
        # custom_loading_script

        # try a ultimate rescue if there was a script
        if custom_loading_script:
            # try:
                self.execute_code_unsafe(custom_loading_script)
            # except: # this does not work I need
            #     super(Image2D, self).__init__(0, 0, 512, 512) # just a rescue to force creation of the file with error tag
            # print('custom_loading_script, self.img', custom_loading_script, self.img)
        if custom_loading_script and self.img:
            # TODO --> avoid code duplication!!! --> TODO -> split my code into plenty of stuff
            if isinstance(self.img, plt.Figure):
                # the passed image is in fact a matplotlib plot --> init super with the corresponding QrectF
                super(Image2D, self).__init__(get_fig_rect(self.img))
                # self.img = self.img
                self.setFigure(self.img)
            # MEGA TODO --> need implement all and make the custom scripyt override all (the only thing I should make sure is that if there is a script it should reach here)


        # we check if the image is properly initialized and if not we raise an Exception
        try:
            self.__init_called__
        except:
            if not allow_unknown_files:
                raise Exception('Image not initialized properly!, super-class __init__() was never called')
            else:
                super(Image2D, self).__init__(0, 0, 512, 512) # create an error image maybe the custom code can be edited later?
            # pass

    # def deepcopy(self):
    #     # Create a new instance of Image2D with the same arguments as the original object
    #     args = (self.x, self.y, self.width, self.height, None, None, self.opacity, self.fill_color, #self.data, self.dimensions
    #             self.placement)
    #     clone = Image2D(*args)
    #
    #     # maybe just do not clone the images beacuse that would take too mych time... all the rest can be kept I guess
    #
    #     # Copy all relevant attributes from the original object to the clone
    #     clone.scale = copy.deepcopy(self.scale)
    #     clone.translation = copy.deepcopy(self.translation)
    #     clone.fill_color = copy.deepcopy(self.fill_color)
    #     clone.img = copy.deepcopy(self.img)
    #     clone.line_style = copy.deepcopy(self.line_style)
    #     clone.annotations = copy.deepcopy(self.annotations)
    #     clone.placement = copy.deepcopy(self.placement)
    #
    #     # Copy crop attributes
    #     clone.crop_left = self.crop_left
    #     clone.crop_right = self.crop_right
    #     clone.crop_top = self.crop_top
    #     clone.crop_bottom = self.crop_bottom
    #
    #     return clone

    def _toBuffer(self, bufferType='raster'):
        if self.img is not None:
            buf = io.BytesIO()
            if bufferType == 'raster':
                self.img.savefig(buf, format='png', bbox_inches='tight')
            else:
                self.img.savefig(buf, format='svg', bbox_inches='tight')
            buf.seek(0)
            return buf
        return None

    # @classmethod
    # def reset_count(cls):
    #     cls._count = 0

    # @return the block incompressible width
    # def getIncompressibleWidth(self):
    #     extra_space = 0  # can add some if boxes around to add text
    #     return extra_space
    #
    # # @return the block incompressible height
    # def getIncompressibleHeight(self):
    #     extra_space = 0  # can add some if boxes around to add text
    #     # do not even do that --> just ignore things
    #     # add box around ???
    #     return extra_space

    def get_extra_border_size(self):
        if self.border_size is not None and self.border_color is not None:
            return self.border_size
        return 0




    # def add_object(self, object, position):
    #     if isinstance(object, list):
    #         for obj in object:
    #             self.add_object(obj, position=position)
    #         return
    #     if position == Image2D.TOP_LEFT:
    #         self.top_left_objects.append(object)
    #     elif position == Image2D.BOTTOM_RIGHT:
    #         self.bottom_right_objects.append(object)
    #     elif position == Image2D.BOTTOM_LEFT:
    #         self.bottom_left_objects.append(object)
    #     elif position == Image2D.CENTERED:
    #         self.centered_objects.append(object)
    #     else:
    #         self.top_right_objects.append(object)

    # TODO --> check if contains it
    # def remove_object(self, object, position):
    #     if position == Image2D.TOP_LEFT:
    #         self.top_left_objects.remove(object)
    #     elif position == Image2D.BOTTOM_RIGHT:
    #         self.bottom_right_objects.remove(object)
    #     elif position == Image2D.BOTTOM_LEFT:
    #         self.bottom_left_objects.remove(object)
    #     elif position == Image2D.CENTERED:
    #         self.centered_objects.remove(object)
    #     else:
    #         self.top_right_objects.remove(object)

    # def remove_all_objects(self, position):
    #     if position == Image2D.TOP_LEFT:
    #         del self.top_left_objects
    #         self.top_left_objects = []
    #     elif position == Image2D.BOTTOM_RIGHT:
    #         del self.bottom_right_objects
    #         self.bottom_right_objects = []
    #     elif position == Image2D.BOTTOM_LEFT:
    #         del self.bottom_left_objects
    #         self.bottom_left_objects = []
    #     elif position == Image2D.CENTERED:
    #         del self.centered_objects
    #         self.centered_objects = []
    #     else:
    #         del self.top_right_objects
    #         self.top_right_objects = []

    # def setLettering(self, letter):
    #     if isinstance(letter, TAText2D):
    #         self.letter = letter
    #     elif isinstance(letter, str):
    #         if letter.strip() == '':
    #             self.letter = None
    #         else:
    #             self.letter = TAText2D(letter)

    # def getRect2D(self):
    #     # self.__class__ = Rect2D
    #     # return super()
    #     # TODO ideally I'd like to get the Rect2D parent but I should think what the best way is to get it...
    #     return self

    def set_rotation(self, theta): # by default set it to black or to None --> white could also be useful
        # self.fill_color = bg_color # , bg_color=0x000000do keep both separated
        super().set_rotation(theta)

    def draw_bg(self, painter, draw=True, parent=None, restore_painter_in_the_end=True):
        # drawing was getting too big so I split the draw bg and draw annotations into two separate things
        if draw:




            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.NoBrush)
            if parent is None:
            # if True:
                painter.setClipRect(self.getRect(
                    scale=True))  # required first to fraw the stuff at the very beginning of it !!! --> it must be done before save
            # for some reason it does not apply to text --> why -−> see how I can apply it

            # if it has a parent then set it to a small size relative to the parent --> in percentage of the parent

            # if parent is not None:
            #     print('I have a parent', parent==self)

            # add a black bg behind the images if needed
            # if self.fill_color is not  None:
            #     print(self.fill_color)
            if self.fill_color is not None:
                # self.fill_color = 0xFFFFFF
                # print('painting fill color')
                painter.setBrush(QBrush(QColor(self.fill_color)))
                painter.drawRect(self.getRect(all=True))

            try:  # trick to force equal save and restore even upon error !!!
                # with QPainter.StateSaver(painter): # much cleaner than painter.save() and painter.restore() --> does not work !!!
                painter.setOpacity(self.opacity)
                # painter.setClipRect(self)  # only draw in self --> very useful for inset borders # pb clip rect does not work for svg --> remove for now users can add it manually if desired or I can add it if people really want it and then I should draw relevant lines or shifted rects --> do that later
                # prevents drawing outside from the image
                #     rect_to_plot = self.boundingRect(scaled=True) #scaled=True #self.adjusted(self.crop_left, self.crop_top, self.crop_right, self.crop_bottom) # need remove the crops with that

                if parent is not None:
                    # MEGA BUG HERE the pb is this stuff is overriding the external placement --> probably I should not do this here

                    # rect_to_plot = self.getRect()
                    # if parent is not None and parent.scale is not None and parent.scale != 1:
                    # rect_to_plot = self.__get_scaled_rect(rect_to_plot, 1. / parent.scale)
                    # rect_to_plot = QRectF(rect_to_plot.x() / parent.scale, rect_to_plot.y() / parent.scale, rect_to_plot.width() / parent.scale,
                    #               rect_to_plot.height() / parent.scale)
                    rect_to_plot = QRectF(0, 0, parent.width(
                        scale=True) * self.fraction_of_parent_image_width_if_image_is_inset, 0)
                    rect_to_plot.setHeight(rect_to_plot.width() / (self.getRect().width() / self.getRect().height()))

                    self.set_to_scale(self.width() / rect_to_plot.width())  # TODO --> CHECK THAT -->  is that ok or should I do the opposite ??? --> this is the only element that needs be rescaled because all the other shold not be changed
                    # rect_to_plot.setHeight(rect_to_plot.height()/parent.scale)
                    # rect_to_plot.setWidth(rect_to_plot.width()/parent.scale)

                    # TODO --> ideally add a border to it -> see how I was doing that and that would require me to -> size is there and I need all the others to be placed relatively to that

                    # rect_to_plot = rect_to_plot.translated(parent.topLeft())
                    rect_to_plot = rect_to_plot.translated(self.topLeft())  # very hacky way to get it to work --> see how I can do that

                    # for some reason this is way too far !!!
                    # print('final', rect_to_plot)
                else:
                    rect_to_plot = self.getRect(scaled=True)  # in that case I can add it a position

                # if parent is not None:
                # rect_to_plot.setX(self.x())
                # rect_to_plot.setY(self.y())

                # print('final_rect_to_plot', rect_to_plot)

                # self.scale = 1
                # if self.scale is not None and self.scale != 1:
                # #     # TODO KEEP THE ORDER THIS MUST BE DONE THIS WAY OR IT WILL GENERATE PLENTY OF BUGS...
                #     new_width = rect_to_plot.width() * self.scale
                #     new_height = rect_to_plot.height() * self.scale
                # #     # print(rect_to_plot.width(), rect_to_plot.height())  # here ok
                # #     # setX changes width --> why is that
                # #
                # #     # TODO BE EXTREMELY CAREFUL AS SETX AND SETY CAN CHANGE WIDTH AND HEIGHT --> ALWAYS TAKE SIZE BEFORE OTHERWISE THERE WILL BE A PB AND ALWAYS RESET THE SIZE WHEN SETX IS CALLED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # #     # Sets the left edge of the rectangle to the given x coordinate. May change the width, but will never change the right edge of the rectangle. --> NO CLUE WHY SHOULD CHANGE WIDTH THOUGH BUT BE CAREFUL!!!
                # #     rect_to_plot.setX(rect_to_plot.x() * self.scale)
                # #     rect_to_plot.setY(rect_to_plot.y() * self.scale)
                # #     # maybe to avoid bugs I should use translate instead rather that set x but ok anyways
                # #     # print(rect_to_plot.width(), rect_to_plot.height())# bug here --> too big
                # #
                # #     # print(new_height, new_height, self.width(), self.scale, self.scale* self.width())
                #     rect_to_plot.setWidth(new_width)
                #     rect_to_plot.setHeight(new_height)

                if self.theta is not None and self.theta != 0:
                    # I have added support for rotation to that maybe I will need something smarter if rotation 90 degrees or flips and images no same width and height
                    painter.translate(rect_to_plot.center())
                    painter.rotate(self.theta)
                    painter.translate(-rect_to_plot.center())

                    # with QPainter.StateSaver(painter):
                    # Calculate the rotation transform
                    # center = rect_to_plot.center()
                    # transform = QTransform().translate(rect_to_plot.center()).rotate(self.theta).translate(
                    #     -center.x(), -center.y())

                    # Apply the transform to the painter
                    # painter.setTransform(transform)

                    # center = rect_to_plot.center()
                    # transform = QTransform().rotate(self.theta, Qt.YAxis).translate(-center.x()/2., -center.y()/2.)
                    # painter.setTransform(transform)

                # ideally I should draw only the content of the

                if self.img is not None and not isinstance(self.img, plt.Figure) and not isinstance(self.img, QSvgRenderer):
                    x = 0
                    y = 0
                    try:
                        w = self.img.get_width()
                        h = self.img.get_height()
                    except:
                        # see how to handle images that are not in the stuff
                        w = self.img.shape[1]
                        h = self.img.shape[0]

                    if w is None or h is None:
                        w = self.img.shape[1]
                        h = self.img.shape[0]

                    if self.crop_top is not None:
                        y = self.crop_top
                        h -= self.crop_top
                    if self.crop_left is not None:
                        x = self.crop_left
                        w -= self.crop_left
                    if self.crop_right is not None:
                        w -= self.crop_right
                    if self.crop_bottom is not None:
                        h -= self.crop_bottom
                    # pb here --> see how to really crop
                    qsource = QRectF(x, y, w, h)

                    # just for debug!!
                    # painter.setBrush(QBrush(QColor(0xFFFF00)))
                    # painter.drawRect(rect_to_plot)
                    # pen = QPen(QColor(self.color))
                    # pen.setWidthF(3)
                    # painter.setPen(pen)

                    # TODO --> maybe have a look here some day https://stackoverflow.com/questions/15166754/stroking-a-path-only-inside-outside

                    if parent is not None and self.border_color is not None and self.border_size is not None and self.border_size >= 1:  # we draw the square first then the image so that the image is not truncated by the bounding rect
                        # outer_rect_margin = 3  # Adjust as needed
                        # Set up the pen for drawing the rectangle

                        pen = QPen(QColor(self.border_color),
                                   self.border_size * 2.)  # Adjust the color and line style as needed
                        # pen.setWidth(outer_rect_margin)  # Set the width of the stroke
                        # pen.setCapStyle(Qt.SquareCap)  # Set the cap style to SquareCap -> draws onlyt outside the rect
                        painter.setPen(pen)
                        # Define the size of the rectangle to draw outside the image

                        # Calculate the coordinates for the outer rectangle
                        # outer_rect_x = rect_to_plot.x() - outer_rect_margin
                        # outer_rect_y = rect_to_plot.y() - outer_rect_margin
                        # outer_rect_width = rect_to_plot.width() + 2 * outer_rect_margin
                        # outer_rect_height = rect_to_plot.height() + 2 * outer_rect_margin

                        # Create a QRect object for the outer rectangle
                        # outer_rect = QRectF(outer_rect_x, outer_rect_y, outer_rect_width, outer_rect_height)

                        # painter.drawRect(outer_rect)
                        painter.drawRect(rect_to_plot)

                    painter.drawImage(rect_to_plot, self.qimage, qsource)  # , flags=QtCore.Qt.AutoColor
                elif self.renderer is not None or isinstance(self.img, plt.Figure):
                    if False:
                        # TODO deactivate this for production but keep it for image editing!
                        pen = QPen(QColor(255, 165, 0))
                        pen.setWidthF(6)
                        painter.setPen(pen)
                        painter.drawRect(
                            rect_to_plot)  # this fills the rect I guess I rather wanna have a pen rather than a brush and a --> probably not what I want !!!

                        # Draw Empty in the center of the rectangle (the shape has no image so it cannot be incorporated)
                        text = "Empty"
                        font = painter.font()  # Use the current font or set a custom font if desired

                        # Calculate the text's center position within the rectangle
                        font_metrics = QFontMetrics(font)
                        text_width = font_metrics.width(text)
                        text_height = font_metrics.height()
                        text_x = rect_to_plot.x() + rect_to_plot.width() / 2. - text_width / 2.
                        text_y = rect_to_plot.y() + rect_to_plot.height() / 2. + text_height / 2.

                        # Draw the text in the middle of the rectangle
                        painter.drawText(int(text_x), int(text_y), text)
                    self.renderer.render(painter, rect_to_plot)
                else:

                    if not check_antialiasing(painter): # only draw this in figure building mode, not in production

                        # print('self.filename',self.filename)
                        # Draw Empty in the center of the rectangle (the shape has no image so it cannot be incorporated)
                        if self.filename is None: # if the file has a name and no image was produced then there is an error somewhere and the user needs to enter custom code to handle things
                            if self.isText:
                                text = 'Label'
                                pen = QPen(QColor(200, 255, 64))  # yellow
                            else:
                                text = "Empty"
                                pen = QPen(QColor(255, 0, 255))  # orange
                        else:
                            text = "Error"
                            pen = QPen(QColor(255, 0, 0))  # orange
                        # TODO deactivate this for production but keep it for image editing!

                        pen.setWidthF(6)
                        painter.setPen(pen)
                        painter.drawRect(rect_to_plot)  # this fills the rect I guess I rather wanna have a pen rather than a brush and a --> probably not what I want !!!

                        font = painter.font()  # Use the current font or set a custom font if desired

                        # Calculate the text's center position within the rectangle
                        font_metrics = QFontMetrics(font)
                        text_width = font_metrics.width(text)
                        text_height = font_metrics.height()
                        text_x = rect_to_plot.x()+ rect_to_plot.width() / 2. - text_width / 2.
                        text_y = rect_to_plot.y()+text_height# + rect_to_plot.height() / 2. + text_height / 2.+text_height # to make it more visible

                        # Draw the text in the middle of the rectangle
                        painter.drawText(int(text_x), int(text_y), text)
            except:
                traceback.print_exc()

            if restore_painter_in_the_end:
                painter.restore()

    def setFigure(self, figure):
        self.must_update_figure_on_first_paint = False

        # TODO load the raw image there so that it can be drawn easily
        # self.figure = figure
        if figure is not None and isinstance(figure, plt.Figure):
            # self.img = self.toImg()
            # print(self.img.get_width())
            # self.qimage = self.img.getQimage()
            # make a renderer out of it and display it ...

            # print("size inches before rendering", figure.get_size_inches())
            # self.figure = figure
            self.img = figure
            buffer = self._toBuffer(bufferType='svg')
            self.renderer = QSvgRenderer(buffer.read())
            buffer.close()
            # self.setSize(QSizeF(self.renderer.defaultSize()))
            # upon init we do set the width --> should this be done here or at other position ??? think about it
            if self.width() == 0:
                size = self.renderer.defaultSize()
                # print('default size', size, 'vs', self.renderer.viewBox())
                self.setWidth(size.width())
                self.setHeight(size.height())
            # self.isSet = True
        elif figure is not None and isinstance(figure, str):  # path to an svg file
            # just try load it
            # do I ever need the buffer for this to cause if yes then I would need to get it --> think how ???

            # if buffer is needed --> this is how I should do it
            # in_file = open(figure)  # opening for [r]eading as [b]inary
            # data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
            # in_file.close()
            # TODO add tries to see if that works and if opened properly
            # print(data)
            self.renderer = QSvgRenderer(figure)  # data --> need convert data to be able to read it
            self.img= self.renderer
            # self.renderer.render(painter, self)# the stuff is a qrectf so that should work
            # self.renderer.setViewBox(viewbox)

            self.filename = figure
            if self.width() == 0:
                size = self.renderer.defaultSize()
                # print('default size', size, 'vs', self.renderer.viewBox())
                self.setWidth(size.width())
                self.setHeight(size.height())
                if size.width() <= 0:
                    logger.error('image "' + str(self.filename) + '" could not be loaded')
                    self.isSet = False
                    return
                # j'arrive pas à faire des crop avec les viewbox
                # viewbox = self.renderer.viewBoxF()
                #
                # # does not really work
                # neo = QRectF()
                # neo.setX(30)
                # neo.setY(30)
                # neo.setHeight(self.height()-30)
                # neo.setWidth(self.width()-30)
                # self.renderer.setViewBox(neo)

            # self.img = None
            # self.isSet = True
        else:
            logger.error(
                'The provided figure is not a valid matplotlib figure nor a valid svg file! Nothing can be done with it... Sorry...')
            # self.img = None
            # self.isSet = False

    def draw_annotations(self,painter, draw=True, parent=None,restore_painter_in_the_end=True):
        try:

            # painter.setClipRect(self.getRect(
            #     scale=True))
            extra_space = 1


            # annots = self.annotations
            # if isinstance(annots, TAText2D):
            #     annots=[annots]


            if  self.annotations is not None and  self.annotations:
                # what I need todo now is a stack per position
                # --> this way I could have as many objects as I want and they will all be stacked --> this will simplify the UI a lot

                # for all positions --> store the last position position and do stuff with it --> TODO

                # or simply use my align class with grouping by position --> that probably makes sense --> see how todo that smartly!!!
                # otherwise I would have to recode all -> is that smart ??? --> maybe it is better to recode still

                # a combination of align and stack would do the job (but I should not use the scale parameter in this case --> I need a small hack !!!
                # it is a weird stack because stack at bottom would require me to place the stuff backward or to reverse it (reversing is easy)

                # I need to group by vertical position top and bottom along with left and right and do the stuff !!!
                # --> see how todo that
                # --> group objects by position and then just place them all at the right position then stack them --> should be easy TODO

                objects_grouped_by_position = groupby_position( self.annotations)

                # print(objects_grouped_by_position)
                # loop smartly over that
                for extra in  self.annotations:
                    # print('extras for image', extra)
                    try:
                        # print('extra.placement', extra.placement.get_position())
                        try:
                            pos = extra.placement.get_position()
                        except:
                            pos = None
                        if pos:
                            # can I do it in a smarter way half coord by half coord ??? -−> maybe yes
                            # TODO --> try to set the element at position --> do one coord at a time so that it is highly portable --> TODO
                            # extra.setTopLeft(self.topLeft()) # by default start with top left as default position
                            if extra.placement.check_position('top'):
                                extra.setTopLeft(extra.x(), self.topLeft().y())
                            if extra.placement.check_position('left'):
                                extra.setTopLeft(self.topLeft().x(), extra.y())
                            if extra.placement.check_position('right'):
                                extra.setTopLeft(self.x() + self.width(all=True) - extra.width(all=True), extra.y())
                            if extra.placement.check_position('bottom'):
                                extra.setTopLeft(extra.x(), self.topLeft().y() + self.height(all=True) - extra.height(
                                    all=True))
                            # print('applying position')
                            # if 'top' in pos and 'left' in pos:
                            #     extra.setTopLeft(self.topLeft())  # TODO REMOVE THAT AND USE SMTHG SMART INSTEAD
                            # elif 'top' in pos and 'right' in pos:
                            #     extra.setTopLeft(self.x()+self.width(scale=True)-extra.width(scale=True), self.topLeft().y())
                            # elif 'bottom' in pos and 'left' in pos:
                            #     extra.setTopLeft(self.x(), self.topLeft().y()+self.height(scale=True)-extra.height(scale=True))
                            # elif 'bottom' in pos and 'right' in pos:
                            #     extra.setTopLeft(self.x()+self.width(scale=True)-extra.width(scale=True), self.topLeft().y() + self.height(scale=True) - extra.height(
                            #     scale=True))
                            if extra.placement.check_position('center_h'):
                                extra.setTopLeft(
                                    self.x() + self.width(all=True) / 2. - extra.width(all=True) / 2., extra.y())
                            if extra.placement.check_position('center_v'):
                                extra.setTopLeft(extra.x(), self.y() + self.height(all=True) / 2. - extra.height(
                                    all=True) / 2.)

                            # if isinstance(extra, Image2D):
                            #     print('indeed it goes there')  # -−> how can I fix it --> but it is not drawn -> see how I can do that I assume I would have o treat them indepently ...
                            #     print(extra.x(), extra.y(), extra.getRect(scale=True))
                        # else:
                        # print('no position to apply')
                        # extra.setTopLeft(self.topLeft().x()+extra.topLeft().x(),self.topLeft().y()+extra.topLeft().y())
                        # extra.setTopLeft(self.topLeft())
                    except:
                        traceback.print_exc()

                    # now for each group I need stack them --> give it a try
                    for group, objects in objects_grouped_by_position.items():
                        if group == ('free', 'relative'):
                            continue
                        else:
                            # stack with or without stuff
                            # for center --> ignore as there is no wa

                            # see how to deal with center --> to me it makes no sense to stack or do anything with them
                            # pack2(1, packing_modes[1], False, *objects) # TODO --> find packing mode from position --> should be doable --> and can ignore

                            # print('objects[0].placement',objects[0].placement)

                            pack2(extra_space, objects[0].placement, True,
                                  *objects)  # TODO --> find packing mode from position --> should be doable --> and can ignore

                    # if isinstance(extra, Line2D):
                    #     print('line is here')

                    # if isinstance(extra, Image2D):
                    #     print('indeed it is there', extra.getRect(scale=True), extra.x(), extra.y(), 'vs',
                    #           rect_to_plot)

                    extra.draw(painter=painter, parent=self)  # added parent for relative plotting

                    # if isinstance(extra, Image2D):
                    #     print('done drawing')
                    #
                    # if False and isinstance(extra, Image2D):
                    #     # MEGA BUG HERE !!!
                    #     print('indeed it is there', extra.getRect(scale=True), extra.x(), extra.y(), 'vs', rect_to_plot)
                    #     painter.setPen(QPen(QColor(0xFF0000)))
                    #     painter.drawRect(extra.getRect(scale=True))
                    #     extra.draw(painter=painter) # ok for some reason I need to do that --> the error is in the rest of the code
                    #     # extra.draw(painter=painter, parent=self) # why it doesn't draw
                    #     # --> I just need to see the placement and place it first

            # draw annotations first
            # if self.annotation is not None and self.annotation:
            #     # need clone the object then set its P1 with respect to position or need a trick to keep original ref and have an updated one just for display but then need renew it all the time --> see how I can do that...
            #     # maybe clone is not smart as it duplicates resources without a need for it
            #     # but then need clone the original rect and draw with respect to that
            #     # and I indeed need scale the shape --> TODO too
            #     # indeed thanks to cloning I always preserve original info --> not bad
            #
            #     # annot position is good
            #     # TODO see how to do that cause not so easy --> think carefully and take inspiration from EZF and improve it
            #     for annot in self.annotation:
            #         # always empty --> why is that
            #         # print('init',annot.get_P1())
            #         # always assume everything is done at 0,0 then do translation
            #         # annot.setTopLeft(self.get_P1().x() + annot.get_P1().x(),                    self.get_P1().y() + annot.get_P1().y())  # always relative to the parent image
            #         # annot.setTopLeft(self.get_P1())  # always relative to the parent image
            #         # print(annot.get_P1())
            #
            #         # print('init', self.get_P1(), 'scale', self.get_scale())
            #         annot.set_to_translation(rect_to_plot.topLeft())
            #         annot.set_to_scale(self.scale)  # will fuck the stuff but ok for a test
            #         # print('scaled',annot.get_P1())
            #         annot.draw(painter=painter)
            #         # print('tranbs', annot.translation)

            # and indeed I need also to take crop into account in order not to misposition things...
            # if self.letter is not None:
            #     self.letter.setTopLeft(rect_to_plot.topLeft().x() + extra_space, rect_to_plot.topLeft().y() + extra_space)

            # then draw text and insets --> on top of annotations
            # TODO need align insets differently than others and need align its bounding box also differently --> TODO but almost there
            # if len(self.top_right_objects) != 0 or len(self.top_left_objects) != 0 or len(
            #         self.bottom_left_objects) != 0 or len(self.bottom_right_objects) != 0 or len(
            #         self.centered_objects) != 0:
            #     # align a scale bar to various positions
            #     # maybe if there is a letter first point should be place below stuff
            #     # top_left = Point2D(self.get_P1())
            #     top_left_shifted = Point2D(rect_to_plot.topLeft())
            #     # top_left_shifted.setX(top_left_shifted.x() )# + extra_space
            #     # top_left_shifted.setY(top_left_shifted.y() )#+ extra_space
            #
            #     # print('before', top_left)
            #     # if self.letter is not None:
            #     #     packY(extra_space, self.letter, top_left_shifted)
            #     # print('after', top_left)
            #
            #     # insets should be aligned to unshifted values
            #     # whereas texts should be aligned to shifted ones
            #     # what if I try all unshifted
            #     # cause in a way it's simpler
            #
            #     # top_right = Point2D(self.get_P1())
            #     top_right_shifted = Point2D(rect_to_plot.topLeft())
            #     top_right_shifted.setX(top_right_shifted.x() + rect_to_plot.width())#- extra_space
            #     top_right_shifted.setY(top_right_shifted.y() )#+ extra_space
            #
            #     # bottom_left = Point2D(self.get_P1())
            #     bottom_left_shifted = Point2D(rect_to_plot.topLeft())
            #     bottom_left_shifted.setX(bottom_left_shifted.x() ) #+ extra_space
            #     bottom_left_shifted.setY(
            #         bottom_left_shifted.y() + rect_to_plot.height() )#- extra_space  # should align right then pack on top of that --> may need a direction in packing--> TODO
            #
            #     bottom_right = Point2D(rect_to_plot.topLeft())
            #     bottom_right_shifted = Point2D(rect_to_plot.topLeft())
            #     bottom_right_shifted.setX(bottom_right_shifted.x() + rect_to_plot.width())# - extra_space
            #     bottom_right_shifted.setY(bottom_right_shifted.y() + rect_to_plot.height())#- extra_space
            #
            #     center = Point2D(rect_to_plot.topLeft())
            #     center.setX(center.x() + rect_to_plot.width() / 2)
            #     center.setY(center.y() + rect_to_plot.height() / 2)
            #
            #     if len(self.top_left_objects) != 0:
            #         # change inset size first
            #         for obj in self.top_left_objects:
            #             if isinstance(obj, Image2D):
            #                 obj.setToWidth(rect_to_plot.width() * obj.fraction_of_parent_image_width_if_image_is_inset)
            #
            #         # if letter exists align with respect to it
            #
            #         alignTop(top_left_shifted, *self.top_left_objects)
            #         alignLeft(top_left_shifted, *self.top_left_objects)
            #
            #         if self.letter is not None:
            #             # packY(extra_space, self.letter, top_left_shifted)
            #             top_left_shifted = self.letter
            #
            #         # in fact images really need be aligned left of the image but the others need be aligned with the letter that has an extra space --> TODO --> change some day
            #
            #         packY(extra_space, top_left_shifted, *self.top_left_objects)
            #
            #         # all images need be shifted back??? to be aligned left
            #
            #         for obj in self.top_left_objects:
            #             # for drawing of inset borders
            #             # if isinstance(obj, Image2D):
            #             #     # make it draw a border and align it
            #             #     # painter.save()
            #             #     img_bounds = Rect2D(obj)
            #             #     img_bounds.stroke = 3
            #             #     # img_bounds.translate(-img_bounds.stroke / 2, -img_bounds.stroke / 2)
            #             #     img_bounds.color = 0xFFFF00
            #             #     img_bounds.fill_color = 0xFFFF00
            #             #     img_bounds.draw(painter=painter)
            #             #     # print(img_bounds)
            #             #     # painter.restore()
            #             obj.draw(painter=painter)
            #
            #     if len(self.top_right_objects) != 0:
            #         # change inset size first
            #         for obj in self.top_right_objects:
            #             if isinstance(obj, Image2D):
            #                 obj.setToWidth(rect_to_plot.width() * obj.fraction_of_parent_image_width_if_image_is_inset)
            #         alignRight(top_right_shifted, *self.top_right_objects)
            #         alignTop(top_right_shifted, *self.top_right_objects)
            #         packY(extra_space, top_right_shifted, *self.top_right_objects)
            #         for obj in self.top_right_objects:
            #             # # for drawing of inset borders
            #             # if isinstance(obj, Image2D):
            #             #     # make it draw a border and align it
            #             #     # painter.save()
            #             #     img_bounds = Rect2D(obj)
            #             #     img_bounds.stroke = 3
            #             #     # img_bounds.translate(img_bounds.stroke / 2, -img_bounds.stroke / 2)
            #             #     img_bounds.color = 0xFFFF00
            #             #     img_bounds.fill_color = 0xFFFF00
            #             #     img_bounds.draw(painter=painter)
            #             #     # print(img_bounds)
            #             #     # painter.restore()
            #             obj.draw(painter=painter)
            #
            #     if len(self.bottom_right_objects) != 0:
            #         # change inset size first
            #         for obj in self.bottom_right_objects:
            #             if isinstance(obj, Image2D):
            #                 obj.setToWidth(rect_to_plot.width() * obj.fraction_of_parent_image_width_if_image_is_inset)
            #         alignRight(bottom_right_shifted, *self.bottom_right_objects)
            #         alignBottom(bottom_right_shifted, *self.bottom_right_objects)
            #         packYreverse(extra_space, bottom_right_shifted, *self.bottom_right_objects)
            #         # packY(3, top_right, *self.top_right_objects) # I do need to invert packing order
            #         for obj in self.bottom_right_objects:
            #             # # for drawing of inset borders
            #             # if isinstance(obj, Image2D):
            #             #     # make it draw a border and align it
            #             #     # painter.save()
            #             #     img_bounds = Rect2D(obj)
            #             #     img_bounds.stroke = 3
            #             #     # img_bounds.translate(-img_bounds.stroke / 2, img_bounds.stroke / 2)
            #             #     # should I clip it to the image size --> maybe it's the best
            #             #     img_bounds.color = 0xFFFF00
            #             #     img_bounds.fill_color = 0xFFFF00
            #             #     img_bounds.draw(painter=painter)
            #             #     # print(img_bounds)
            #             #     # painter.restore()
            #             obj.draw(painter=painter)
            #
            #     if len(self.bottom_left_objects) != 0:
            #         # change inset size first
            #         for obj in self.bottom_left_objects:
            #             if isinstance(obj, Image2D):
            #                 obj.setToWidth(rect_to_plot.width() * obj.fraction_of_parent_image_width_if_image_is_inset)
            #         alignLeft(bottom_left_shifted, *self.bottom_left_objects)
            #         alignBottom(bottom_left_shifted, *self.bottom_left_objects)
            #         packYreverse(extra_space, bottom_left_shifted, *self.bottom_left_objects)
            #         for obj in self.bottom_left_objects:
            #             # # for drawing of inset borders
            #             # if isinstance(obj, Image2D):
            #             #     # make it draw a border and align it
            #             #     # painter.save()
            #             #     img_bounds = Rect2D(obj)
            #             #     img_bounds.stroke = 3
            #             #     # img_bounds.translate(-img_bounds.stroke/2, img_bounds.stroke/2)
            #             #     img_bounds.color = 0xFFFF00
            #             #     img_bounds.fill_color = 0xFFFF00
            #             #     img_bounds.draw(painter=painter)
            #             #     # print(img_bounds)
            #             #     # painter.restore()
            #             obj.draw(painter=painter)
            #
            #     if len(self.centered_objects) != 0:
            #         # change inset size first
            #         for obj in self.centered_objects:
            #             if isinstance(obj, Image2D):
            #                 obj.setToWidth(rect_to_plot.width() * obj.fraction_of_parent_image_width_if_image_is_inset)
            #         alignCenterH(center, *self.centered_objects)
            #         alignCenterV(center, *self.centered_objects)
            #         for obj in self.centered_objects:
            #             # # for drawing of inset borders
            #             # if isinstance(obj, Image2D):
            #             #     # make it draw a border and align it
            #             #     # painter.save()
            #             #     img_bounds = Rect2D(obj)
            #             #     img_bounds.stroke = 3
            #             #     img_bounds.color = 0xFFFF00
            #             #     img_bounds.fill_color = 0xFFFF00
            #             #     img_bounds.draw(painter=painter)
            #             #     # print(img_bounds)
            #             #     # painter.restore()
            #             obj.draw(painter=painter)

            # then need to draw the letter at last so that it is always on top
            # if self.letter is not None:
            #     self.letter.draw(painter)
        except:
            traceback.print_exc()

        if restore_painter_in_the_end:
            painter.restore()
    def draw(self, painter, draw=True, parent=None):
        if draw:

                # TODO --> shall I recover and reuse the rect ???

            self.draw_bg(painter, draw=draw, parent=parent, restore_painter_in_the_end=False)

                # letter is good
                # then position all of them as a chain --> TODO
            self.draw_annotations(painter, draw=draw, parent=parent, restore_painter_in_the_end=False)

            painter.restore()

    # def __or__(self, other):
    #     from epyseg.figure.row import Row  # KEEP Really required to avoid circular imports
    #     return Row(self, other)
    #
    # # create a Fig with divide
    # # def __truediv__(self, other):
    # def __truediv__(self, other):
    #     from epyseg.figure.column import Column  # KEEP Really required to avoid circular imports
    #     return Column(self, other)
    #
    # def __floordiv__(self, other):
    #     return self.__truediv__(other=other)

    # ai je vraiment besoin de ça ? en fait le ratio suffit et faut aussi que j'intègre le crop sinon va y avoir des erreurs
    # Force the montage width to equal 'width_in_px'
    def setToWidth(self, width_in_px):
        # pure_image_width = self.width()
        # ratio = width_in_px / pure_image_width
        # self.setWidth(width_in_px)
        # self.setHeight(self.height() * ratio)
        # # we recompute the scale for the scale bar # TODO BE CAREFUL IF EXTRAS ARE ADDED TO THE OBJECT AS THIS WOULD PERTURB THE COMPUTATIONS
        # self.update_scale()
        pure_image_width = self.width(scaled=False)# need original height and with in fact
        # if self.crop_left is not None:
        #     pure_image_width -= self.crop_left
        # if self.crop_right is not None:
        #     pure_image_width -= self.crop_right
        scale = width_in_px / pure_image_width
        self.scale = scale


    def setToHeight(self, height_in_px):
        # pure_image_height = self.height()
        # self.setHeight(height_in_px)
        # ratio = height_in_px / pure_image_height
        # self.setWidth(self.width() * ratio)
        # # we recompute the scale for the scale bar # TODO BE CAREFUL IF EXTRAS ARE ADDED TO THE OBJECT AS THIS WOULD PERTURB THE COMPUTATIONS
        # self.update_scale()
        pure_image_height = self.height(scaled=False)
        # if self.crop_top is not None:
        #     pure_image_height-=self.crop_top
        # if self.crop_bottom is not None:
        #     pure_image_height-=self.crop_bottom
        scale = height_in_px/pure_image_height
        self.scale = scale
        # need update bounds
        # scale is ok

    # def update_scale(self):
    #     # we recompute the scale for the scale bar # TODO BE CAREFUL IF EXTRAS ARE ADDED TO THE OBJECT AS THIS WOULD PERTURB THE COMPUTATIONS
    #     self.scale = self.get_scale()

    # def get_scale(self):
    #     # we recompute the scale for the scale bar # TODO BE CAREFUL IF EXTRAS ARE ADDED TO THE OBJECT AS THIS WOULD PERTURB THE COMPUTATIONS
    #     return self.width() / self.img.get_width()

    def crop(self, left=None, right=None, top=None, bottom=None, all=None):
        # print(self.boundingRect())
        if left is not None:
            self.crop_left = left
            # self.setWidth(self.img.get_width() - self.crop_left)
        if right is not None:
            self.crop_right = right
            # self.setWidth(self.img.get_width() - self.crop_right)
        if top is not None:
            self.crop_top = top
            # self.setHeight(self.img.get_height() - self.crop_top)
        if bottom is not None:
            self.crop_bottom = bottom
            # self.setHeight(self.img.get_height() - self.crop_bottom)
        if all is not None:
            self.crop_left = all
            self.crop_right = all
            self.crop_top = all
            self.crop_bottom = all
            # self.setWidth(self.img.get_width() - self.crop_left)
            # self.setWidth(self.img.get_width() - self.crop_right)
            # self.setHeight(self.img.get_height() - self.crop_top)
            # self.setHeight(self.img.get_height() - self.crop_bottom)

        # see how to crop actually because I need to create a qimage
        # self.qimage = self.img.crop()
        # print(self.boundingRect())
    # def set_to_scale(self, factor):
    #     self.scale = factor

    def set_to_translation(self, translation):
        self.translation = translation

    # WHY 0,0 FOR BOUNDS ??? --> sounds not smart to me
    def boundingRect(self, scaled=True):
 # en fait pas good besoin de prendre les crops et le scale en compte
        # is
        # rect_to_plot = self.adjusted(self.crop_left, self.crop_top, -self.crop_right, -self.crop_bottom)
        rect_to_plot = self.adjusted(0, 0, -self.crop_right-self.crop_left, -self.crop_bottom-self.crop_top)
        # rect_to_plot = self.adjusted(-self.crop_left, -self.crop_top, -self.crop_right, -self.crop_bottom)
        # rect_to_plot = self.adjusted(0,0,0,0)
        # print('begin rect_to_plot', rect_to_plot, self.scale)
        # if kwargs['draw']==True or kwargs['fill']==True:
        # if self.scale is None or self.scale==1:
        #     painter.drawRect(self)
        # else:
        # on clone le rect
        if self.scale is not None and self.scale != 1 and scaled:
            # TODO KEEP THE ORDER THIS MUST BE DONE THIS WAY OR IT WILL GENERATE PLENTY OF BUGS...
            new_width = rect_to_plot.width() * self.scale
            new_height = rect_to_plot.height() * self.scale
            # print(rect_to_plot.width(), rect_to_plot.height())  # here ok
            # setX changes width --> why is that

            # TODO BE EXTREMELY CAREFUL AS SETX AND SETY CAN CHANGE WIDTH AND HEIGHT --> ALWAYS TAKE SIZE BEFORE OTHERWISE THERE WILL BE A PB AND ALWAYS RESET THE SIZE WHEN SETX IS CALLED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Sets the left edge of the rectangle to the given x coordinate. May change the width, but will never change the right edge of the rectangle. --> NO CLUE WHY SHOULD CHANGE WIDTH THOUGH BUT BE CAREFUL!!!
            # rect_to_plot.setX(rect_to_plot.x() * self.scale)
            # rect_to_plot.setY(rect_to_plot.y() * self.scale)
            # maybe to avoid bugs I should use translate instead rather that set x but ok anyways
            # print(rect_to_plot.width(), rect_to_plot.height())# bug here --> too big

            # print(new_height, new_height, self.width(), self.scale, self.scale* self.width())
            rect_to_plot.setWidth(new_width)
            rect_to_plot.setHeight(new_height)
        return rect_to_plot

    # def setTopLeft(self, *args):
    #     if not args:
    #         logger.error("no coordinate set...")
    #         return
    #     if len(args) == 1:
    #         self.moveTo(args[0].x(), args[0].y())
    #     else:
    #         self.moveTo(QPointF(args[0], args[1]))

    # def get_P1(self):
    #     return self.boundingRect().topLeft()
    #
    # def width(self, scaled=True):
    #     return self.boundingRect(scaled=scaled).width()
    #
    # def height(self, scaled=True):
    #     return self.boundingRect(scaled=scaled).height()

    SVG_INKSCAPE = 96
    SVG_ILLUSTRATOR = 72

    # NB THIS CODE IS BASED ON THE EZFIG SAVE CODE --> ANY CHANGE MADE HERE MAY ALSO BE MADE TO THE OTHER
    # best here would be for image to keep original size if nothing is specified
    # could also make it return a qimage for display in pyTA
    # qualities = [QPainter.NonCosmeticDefaultPen,  QPainter.SmoothPixmapTransform, QPainter.TextAntialiasing,QPainter.Antialiasing,QPainter.HighQualityAntialiasing]
    # qualities = [  QPainter.SmoothPixmapTransform, QPainter.TextAntialiasing,QPainter.Antialiasing] # painter.setRenderHint
    qualities = [QPainter.SmoothPixmapTransform, QPainter.TextAntialiasing, None, QPainter.Antialiasing] # None sets antialiasing to False -−> see code after # painter.setRenderHint  QPainter.HighQualityAntialiasing,

    '''
    Here are some common interpolation modes:

Qt.SmoothPixmapTransform: This mode enables smooth transformation of pixmaps when they are scaled or rotated. It uses bilinear or bicubic interpolation to provide smoother results, which can be useful when resizing images or drawing rotated content. However, this mode may have a performance impact, especially when dealing with large images or complex transformations.
Qt.HighQualityAntialiasing: This mode enables high-quality antialiasing for painting operations. Antialiasing helps to reduce the jagged appearance of diagonal lines and curves by smoothing their edges. This mode can be useful when drawing shapes, text, or other graphical elements that require smooth edges. However, it may also have a performance impact, especially when dealing with complex scenes or large-scale drawings.
Qt.TextAntialiasing: This mode enables antialiasing specifically for text rendering. It can help to improve the readability and appearance of text in your application, especially at small font sizes or when using custom fonts. However, it may also have a performance impact, especially when dealing with large amounts of text or complex text layouts.

painter = QPainter(some_widget)
painter.setRenderHint(Qt.SmoothPixmapTransform)
# or
painter.setRenderHint(Qt.HighQualityAntialiasing)
# or
painter.setRenderHint(Qt.TextAntialiasing)

painter.setRenderHints(Qt.SmoothPixmapTransform | Qt.HighQualityAntialiasing)
    '''
    def save(self, path, filetype=None, title=None, description=None, svg_dpi=SVG_INKSCAPE, quality=qualities[-1]):
        # if path is None or not isinstance(path, str):
        #     logger.error('please provide a valide path to save the image "' + str(path) + '"')
        #     return
        if path is None:
            filetype = '.tif'

        if filetype is None:
            if path.lower().endswith('.svg'):
                filetype = 'svg'
            else:
                filetype = os.path.splitext(path)[1]
        dpi = 72  # 300 # inkscape 96 ? check for illustrator --> check

        if filetype == 'svg':
            generator = QSvgGenerator()
            generator.setFileName(path)
            if svg_dpi == self.SVG_ILLUSTRATOR:
                generator.setSize(QSize(595, 842))
                generator.setViewBox(QRect(0, 0, 595, 842))
            else:
                generator.setSize(QSize(794, 1123))
                generator.setViewBox(QRect(0, 0, 794, 1123))

            if title is not None and isinstance(title, str):
                generator.setTitle(title)
            if description is not None and isinstance(description, str):
                generator.setDescription(description)
            generator.setResolution(
                svg_dpi)  # fixes issues in inkscape of pt size --> 72 pr illustrator and 96 pr inkscape but need change size

            painter = QPainter(generator)

            # print(generator.title(), generator.heightMM(), generator.height(), generator.widthMM(),
            #       generator.resolution(), generator.description(), generator.logicalDpiX())
        else:
            scaling_factor_dpi = 1
            # scaling_factor_dpi = self.scaling_factor_to_achieve_DPI(300)

            # in fact take actual page size ??? multiplied by factor
            # just take real image size instead


            # image = QtGui.QImage(QSize(self.cm_to_inch(21) * dpi * scaling_factor_dpi, self.cm_to_inch(29.7) * dpi * scaling_factor_dpi), QtGui.QImage.Format_RGBA8888) # minor change to support alpha # QtGui.QImage.Format_RGB32)

            # NB THE FOLLOWING LINES CREATE A WEIRD ERROR WITH WEIRD PIXELS DRAWN some sort of lines NO CLUE WHY

            img_bounds = self.boundingRect()
            # image = QtGui.QImage(QSize(img_bounds.width() * scaling_factor_dpi, img_bounds.height()* scaling_factor_dpi),  QtGui.QImage.Format_RGBA8888)  # minor change to support alpha # QtGui.QImage.Format_RGB32)
            image = QtGui.QImage(QSize(int(img_bounds.width() * scaling_factor_dpi), int(img_bounds.height()* scaling_factor_dpi)),  QtGui.QImage.Format_RGBA8888)  # minor change to support alpha # QtGui.QImage.Format_RGB32)
            # image = QtGui.QImage(QSize(int(img_bounds.scale(scaling_factor_dpi))),  QtGui.QImage.Format_RGBA8888)  # minor change to support alpha # QtGui.QImage.Format_RGB32)
            # print('size at dpi',QSize(img_bounds.width() * scaling_factor_dpi, img_bounds.height()* scaling_factor_dpi))
            # QSize(self.cm_to_inch(0.02646 * img_bounds.width())
            # self.cm_to_inch(0.02646 * img_bounds.height())
            # need convert pixels to inches
            # is there a rounding error

            # force white bg for non jpg
            try:
                # print(filetype.lower())
                # the tif and png file formats support alpha
                if not filetype.lower() == '.png' and not filetype.lower() == '.tif' and not filetype.lower() == '.tiff':
                    image.fill(QColor.fromRgbF(1,1,1))
                else:
                    # image.fill(QColor.fromRgbF(1, 1, 1, alpha=1))
                    # image.fill(QColor.fromRgbF(1, 1, 1, alpha=1))
                    # TODO KEEP in fact image need BE FILLED WITH TRANSPARENT OTHERWISE GETS WEIRD DRAWING ERRORS
                    # TODO KEEP SEE https://stackoverflow.com/questions/13464627/qt-empty-transparent-qimage-has-noise
                    # image.fill(qRgba(0, 0, 0, 0))
                    image.fill(QColor.fromRgbF(0,0,0,0))
            except:
                pass
            painter = QPainter(image)  # see what happens in case of rounding of pixels
            # painter.begin()
            painter.scale(scaling_factor_dpi, scaling_factor_dpi)
        if quality is not None:
            painter.setRenderHint(quality)  # to improve rendering quality
        else:
            painter.setRenderHint(QPainter.Antialiasing, False)  # to improve rendering quality
        self.draw(painter)
        painter.end()
        if path is None:
            return image
        if filetype != 'svg':
            image.save(path)
            return image

    #based on https://stackoverflow.com/questions/19902183/qimage-to-numpy-array-using-pyside
    def convert_qimage_to_numpy(self, qimage):
        qimage = qimage.convertToFormat(QtGui.QImage.Format.Format_RGB32)
        width = qimage.width()
        height = qimage.height()
        image_pointer = qimage.bits() # creates a deep copy --> this is what I want
        # image_pointer.setsize(qimage.byteCount())
        try:
            image_pointer.setsize(qimage.sizeInBytes()) # qt6 version of the stuff
        except:
            image_pointer.setsize(qimage.byteCount())
        # arr = np.array(image_pointer,copy=True).reshape(height, width, 4)
        arr = np.array(image_pointer).reshape(height, width, 4)
        arr = arr[..., 0:3]
        arr = RGB_to_BGR(arr)  # that seems to do the job
        return arr
    # def convert_qimage_to_numpy(self,qimage):
    #     """Convert a QImage object to a NumPy array.
    #
    #     Args:
    #         qimage (QImage): The QImage object to convert.
    #
    #     Returns:
    #         numpy.ndarray: The NumPy array representation of the QImage.
    #     """
    #     # get the image dimensions
    #     height, width, channels = qimage.height(), qimage.width(), qimage.format().channelCount()
    #
    #     # create a buffer object from the image data
    #     buffer = qimage.constBits()
    #     buffer.setsize(
    #         buffer.nbytes)  # set the size of the buffer to the number of bytes required to store the image data
    #
    #     # create a NumPy array from the buffer object
    #     array = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, channels))
    #
    #     # return the NumPy array
    #     return array

    # simple equation for an image
    # or maybe ask for starting expression
    # autoincrement math to get the right value
    # def _get_width_equation(self):
    #     # incr = fig_tools.common_value
    #     # AR = self.width(False)/self.height(False)
    #     # variable =
    #     equa_w = Symbol('a'+str(id(self)))*self.width(False)+0
    #     # equa_h = variable*AR*self.width(False)+0
    #     # incr+=1
    #     # fig_tools.common_value = incr
    #     return equa_w #, equa_h

    # def _get_height_equation(self):
    #     # incr = fig_tools.common_value
    #     AR = self.width(False)/self.height(False)
    #     # equa_w = Symbol('a'+str(id(self)))*self.width(False)+0
    #     equa_h = Symbol('a'+str(id(self)))*AR*self.width(False)+0
    #     # incr+=1
    #     # fig_tools.common_value = incr
    #     return equa_h #, equa_h

    # use that so that I can expand
    # if unique --> do nothing if many see how to handle that???
    # see how
    # def get_equation(self):
    #     from sympy import nsolve, exp, Symbol
    #     AR = self.width(False)/self.height(False)
    #     equa_w = Symbol('a'+str(id(self)))*self.width(False)+0
    #     equa_h = Symbol('a'+str(id(self)))*AR*self.width(False)+0
    #     return [equa_w] , [equa_h], None # equa in width, equa in height, equas to solve, not useful here though

    # def contains(self, *__args):
    #     # print('I was called in there')
    #     # return super().contains(*__args)
    #     return self.getRect(all=True).__contains__(*__args)

    def draw_inner_layout_selection(self, painter):
        painter.save()
        try:
            rect = self.getRect(scale=True)
            painter.setPen(QPen(QColor(0, 255, 255)))
            painter.drawRect(rect)
        except:
            print('inner error')
            traceback.print_exc()
        painter.restore()

    def __contains__(self, item):
        return False

    # maybe TODO !!!
    # allow to deepcopy and copy
    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    # be careful with that because this is what is compared when using == !!! so if poorly implemented this can have dramatic effects
    def __str__(self):
    #     return f"{ self.__class__.__name__} {self.ID}"
        return self.__repr__()
    #
    # def __repr__(self):
    #     return self.__str__()
    def __repr__(self):
        class_name = type(self).__name__
        memory_address = hex(id(self))
        if self.isText:
            class_name = 'Label_' + class_name
        elif isinstance(self.img, plt.Figure):
            class_name = 'Fig_' + class_name
        elif self.renderer is not None:
            class_name = 'SVG_'+class_name
        elif self.img is None and self.filename is not None:
            class_name = 'Error_'+class_name
        elif self.img is None:
            class_name = 'Empty_'+class_name

        if self.filename is not None:
            base_name = os.path.basename(self.filename)
            return f"{class_name}-{memory_address}-{base_name}"
        return f"{class_name}-{memory_address}"

    def to_dict(self):
        x = self.x()
        y = self.y()
        width = self.width()
        height = self.height()

        # Create a dictionary representation of the values of the super object
        output_dict = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            # 'args':self.filename,
            'filename':self.filename,
        }
        # Update the dictionary with the __dict__ of Rectangle2D
        output_dict.update(self.__dict__)
        return output_dict


    def execute_code_unsafe(self, code, parent=None): # TODO --> see how to handle the security!!!
        local_namespace = {'plt': plt, 'Img': Img, 'np':np} # all imports should be made there (otherwise the user needs to do the imports himslef --> painful though
        try:
            exec(code, locals(), local_namespace)
            if 'self.img' in local_namespace:  # that works also with self --> do this specifically for the image stuff
                self.img = local_namespace['self.img'] # shall I transfer more things !!!
            # I may need to recover many more parameters
        except Exception as e:
            print("Error:", e)

    # def isText(self):
    #     # Check if the annotations attribute is a list or None
    #     # if isinstance(self.annotations, list) or self.annotations is None:
    #     #     return False
    #
    #     # Check if the annotations attribute is a TAText2D object
    #     if isinstance(self.annotations, TAText2D):
    #         return True
    #
    #     # If the annotations attribute is neither a list, None, nor a TAText2D object
    #     # else:
    #     #     print('The object is neither an image nor a text file')
    #     return False


if __name__ == '__main__':
    app = QApplication(sys.argv)# IMPORTANT KEEP !!!!!!!!!!!

    if True:
        # Data for plotting
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        fig, ax = plt.subplots()
        print(type(fig))
        ax.plot(t, s)

        ax.set(xlabel='time (s)', ylabel='voltage (mV)', title=None)
        ax.grid()

        figure = Image2D(fig)



        sys.exit(0)

    if True:
        # todo test the use of an empty image with given dimensions then once this is done try to do stuff
        # in fact in all cases the only thing that matters is the initial rect --> I could put a rect instead of an image and that would give me all the things I need
        # TODO

        # try to do that
        try:
            empty_img = Image2D()
            print(empty_img.width())
        except:
            traceback.print_exc()
            print('test that empty images are not allowed')

        # do I already have a construction that would do the job
        empty_img = Image2D(width=120, height=240)# that seems to work --> but super is never called --> see
        # maybe allow an image to be initialized by a rect (to act as an empty image and if that is the case the image could be replaced) by what I need !!!

        print(empty_img)
        print(empty_img.width())

        sys.exit(0)

    # is it possible that I never implemented the rotation ???
    # can I do it???

    # VERY GOOD --> I HAVE FINALLY FIXED IT

    # ça marche --> voici deux examples de shapes
    test = Image2D(x=12, y=0, width=100, height=100)  # could also be used to create empty image with

    print(test.img)
    print(test.boundingRect())
    # print(test.get_P1().x())

    # bug qd on definit une image comme param
    # test = Image2D('/E/Sample_images/counter/06.png')
    test = Image2D('/E/Sample_images/counter/01.png')
    print(test.boundingRect())  # --> it is ok there so why not below # not callable --> why -->
    # print(test.get_P1())  # ça marche donc où est le bug
    # print(test.get_P1().y())  # ça marche donc où est le bug
    # print(test.getP1().width())
    # ça marche

    # try draw on the image the quivers
    # img0.setLettering('<font color="red">A</font>')
    # # letter
    # img0.annotation.append(Rect2D(88, 88, 200, 200, stroke=3, color=0xFF00FF))
    # img0.annotation.append(Ellipse2D(88, 88, 200, 200, stroke=3, color=0x00FF00))
    # img0.annotation.append(Circle2D(33, 33, 200, stroke=3, color=0x0000FF))

    test.annotations.append(TAText2D('<font color="red">A</font>', placement='top-left'))

    test.annotations.append(Line2D(33, 33, 88, 88, stroke=3, color=0x0000FF))

    test.annotations.append(Line2D(128, 33, 88, 88, stroke=0.65, color=0xFFFF00))
    # img0.annotation.append(Freehand2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
    # # img0.annotation.append(PolyLine2D(10, 10, 20, 10, 20, 30, 288, 30, color=0xFFFF00, stroke=3))
    # img0.annotation.append(Point2D(128, 128, color=0xFFFF00, stroke=6))

    # add a save to the image --> so that it exports as a raster --> TODO


    # painter =
    # img = test.draw() # if no painter --> create one as not to lose any data and or allow to save as vectorial


    img = test.save('/E/trash/test_line2D.tif')

    # test.save('/E/Sample_images/sample_images_PA/mini_vide/analyzed/trash/test_line2D.svg')

    #trop facile --> just hack it so that it can return a single qimage # or return a numpy image that is then plotted -> should not be too hard !!! I think --> TODO
    img = test.convert_qimage_to_numpy(img) # --> ok but I just need to swap the channels then I'll be done --> try that maybe with plenty of input images just to see

    # empty image work --> now try to see if I can create an image from a Figure and or a vector graphic ??? -−> TODO

    # shall I save
    # try with non RGB images just to see

    # img = RGB_to_BGR(img)

    # almost there --> just need to check that the size of the image is ok and that everything is fine
    plt.imshow(img)
    plt.show()


    print('here')
    img2 = Image2D('/E/Sample_images/counter/02.png')
    print('here3')
    preview(img2)

    # test replace the plot of pyTA of the polarity by this one --> should be quite easy TODO I think --> TODO

    # ok --> it all seems to work --> see how I can handle that



    # --> all seems ok now
    # --> put this in the advanced sql plotter

