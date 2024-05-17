from epyseg.figure.alignment import pack2, align2, align_positions
from epyseg.draw.shapes.rectangle2d import Rectangle2D
from epyseg.draw.shapes.txt2d import TAText2D
from epyseg.draw.shapes.Position import Position
# logger
from epyseg.tools.logger import TA_logger

logger = TA_logger()

class ScaleBar(Rectangle2D):

    # TODO need a scaling factor for the bar if image is itself scaled or ??? --> most likely yes need think about it
    # TODO handle bar color
    def __init__(self, bar_width_in_units=0, legend="", unit_to_pixel_conversion_factor=1, bar_height_in_px=3, placement=Position('bottom-right'), **kwargs):
        super(ScaleBar, self).__init__()
        self.scale = 1
        self.bar = Rectangle2D(color=None, fill_color=0xFFFFFF, stroke=0)
        self.bar.setWidth(bar_width_in_units * unit_to_pixel_conversion_factor)
        self.bar.setHeight(bar_height_in_px)
        self.legend = None
        self.setLegend(legend)
        self.bar_width_in_units = bar_width_in_units
        self.unit_to_pixel_conversion_factor = unit_to_pixel_conversion_factor
        if not isinstance(placement, Position):
            placement = Position(placement)
        self.placement = placement
        self.line_style = None # useless but require for compat with other shapes

    def setLegend(self, legend):
        if isinstance(legend, str):
            self.legend = TAText2D(legend)
        elif isinstance(legend, TAText2D):
            self.legend = legend
        else:
            self.legend = None

    def setBarWidth(self, bar_width_in_units):
        self.bar_width_in_units = bar_width_in_units

    def setConversionFactor(self, unit_to_pixel_conversion_factor):
        self.unit_to_pixel_conversion_factor = unit_to_pixel_conversion_factor

    def draw(self, painter, draw=True, parent=None):
        self.bar.draw(painter=painter)
        if self.legend is not None:
            self.legend.draw(painter=painter)
        # self.drawAndFill(painter=painter)

    def updateBoudingRect(self):
        """
        updates the image bounding rect depending on content
        :return:
        """

        # contient deux objects et est donc la somme des deux
        # --> facile en theorie faire que du packing et de l'alignement à gauche droite ou ailleurs
        # pack in y direction the text and the bar
        # extra_space_below = 3 # TODO see how to make it not stuck to the bottom of the image --> it needs be a specificity of the bar and text but not for images --> TODO -> see how to do that
        x = None
        y = None
        x2 = None
        y2 = None

        to_pack = [self.bar, self.legend]
        for img in to_pack:
            if img is None:
                continue
            topLeft = img.topLeft()
            if x is None:
                x = topLeft.x()
            if y is None:
                y = topLeft.y()
            x = min(topLeft.x(), x)
            y = min(topLeft.y(), y)

            # print(img, img.boundingRect(), type(img))
            # print(img, img.boundingRect(), type(img), img.boundingRect().height())

            if x2 is None:
                x2 = topLeft.x() + img.boundingRect().width()
            if y2 is None:
                y2 = topLeft.y() + img.boundingRect().height()
            x2 = max(topLeft.x() + img.boundingRect().width(), x2)
            y2 = max(topLeft.y() + img.boundingRect().height(), y2)

        self.setX(x)
        self.setY(y)
        self.setWidth(x2 - x)
        self.setHeight(y2 - y)
        # self.setHeight(self.height()+extra_space_below)



    def packY(self, space=3):
        # center in vertical axis then pack
        #
        # last_x = 0
        # last_y = 0
        #
        # to_pack = [self.bar, self.legend]
        # for i in range(len(to_pack)):
        #     img = self.images[i]
        #     if i != 0:
        #         last_y += space
        #     img.setTopLeft(img.topLeft().x(), last_y)
        #     # get all the bounding boxes and pack them with desired space in between
        #     # get first point and last point in x
        #     x = img.boundingRect().x()
        #     y = img.boundingRect().y()
        #     last_x = img.boundingRect().x() + img.boundingRect().width()
        #     last_y = img.boundingRect().y() + img.boundingRect().height()
        if self.legend is not None:
            self.bar.setWidth(self.scale * self.bar_width_in_units * self.unit_to_pixel_conversion_factor)
            # alignCenterH(self.legend, self.bar)
            align2(align_positions[-1], self.legend, self.bar)
            # align_positions = ['Top', 'Bottom', 'Left', 'Right', 'CenterV', 'CenterH']
            # packY(12, self.legend, self.bar)
            pack2(3, ('-' if self.placement.check_position('top') else '') + 'Y', False, self.legend, self.bar)

        self.updateBoudingRect()

    # finally just need align right

    def setTopLeft(self, *args):
        # TODO check this code as most of this si probably totally useless
        self.packY()
        curP1 = self.topLeft()
        Rectangle2D.setTopLeft(self, *args)
        newP1 = self.topLeft()

        to_pack = [self.bar, self.legend]
        for img in to_pack:
            if img is not None:
                img.translate(newP1.x() - curP1.x(), newP1.y() - curP1.y())

        self.updateBoudingRect()

    # def set_to_scale(self, scale):
    #     self.scale = scale

    # def setcolor

    # get the bounds of the bar with the associated text
    # center text on bar see how I do in EZF

    def __repr__(self):
        class_name = type(self).__name__
        memory_address = hex(id(self))
        return f"{class_name}-{memory_address}"