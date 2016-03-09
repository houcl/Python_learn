# -*- coding: utf-8 -*-

class RGBDeal(object):

    #色彩转换
    def RGBToHTMLColor(self, rgb_tuple):
        """ convert an (R, G, B) tuple to #RRGGBB """

        hexcolor = '#%02x%02x%02x' % rgb_tuple

        # that's it! '%02x' means zero-padded, 2-digit hex values

        return hexcolor

    def HTMLColorToRGB(self, colorstring):
        """ convert #RRGGBB to an (R, G, B) tuple """

        colorstring = colorstring.strip()

        if colorstring[0] == '#': colorstring = colorstring[1:]

        if len(colorstring) != 6:
            return ValueError, "input #%s is not in #RRGGBB format" % colorstring

        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]

        return (r, g, b)

    def HTMLColorToPILColor(self, colorstring):
        """ converts #RRGGBB to PIL-compatible integers"""

        colorstring = colorstring.strip()

        while colorstring[0] == '#': colorstring = colorstring[1:]
        # get bytes in reverse order to deal with PIL quirk
        colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
        # finally, make it numeric
        color = int(colorstring, 16)

        return color

    def PILColorToRGB(self, pil_color):
        """ convert a PIL-compatible integer into an (r, g, b) tuple """
        hexstr = '%06x' % pil_color
        # reverse byte order
        r, g, b = hexstr[4:], hexstr[2:4], hexstr[:2]
        r, g, b = [int(n, 16) for n in (r, g, b)]

        return (r, g, b)

    def PILColorToHTMLColor(self, pil_integer):
        k = DataDeal.PILColorToRGB(pil_integer)
        q = DataDeal.RGBToHTMLColor(k)
        return q

    def RGBToPILColor(self, rgb_tuple):
        return HTMLColorToPILColor(RGBToHTMLColor(rgb_tuple))
