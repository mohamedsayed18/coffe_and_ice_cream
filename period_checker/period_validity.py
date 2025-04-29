# How to define valid or not valid period
# according to the DASH format documentation https://developers.broadpeak.io/docs/foundations-dash#periods
# It could be programaticaly wrong

'''
It could be sematic wrong due to any of the following:
* time
* Each Period contains one or multiple Adaptation Sets.
* Each Adaptation Set contains one or multiple Representations.
* Is it a must? A Representation is composed of multiple Segments. They contain the actual media being played back by the video player.
*
'''
import xml.etree.ElementTree as ET


def valid_period(period: ET.ElementTree) -> bool:
    # check adaptationset
    root = period.getroot()
    adaptationset = root.findall('AdaptationSet')
    if not adaptationset:
        print('Invalid Period, no adaptationset')
        return False

    # check representation
    for child in adaptationset:
        representations = child.findall('Representation')
        if not representations:
            print('Invalid period, No representation')
            return False

    # check segment template
    for rep in representations:
        seg_template = rep.find('SegmentTemplate')
        if seg_template is not None:
            media = seg_template.attrib.get('media')
            if not media:
                print('Invalid period, No media')
                return False
            elif '$Number$' not in media and '$Time$' not in media:
                print('Invalid period, No Number or times format')
                return False

            initialization = seg_template.attrib.get('initialization')
            if not initialization:
                print('Invalid period, No initialization')
                return False

        else:
            print('Invalid period, No segment template')
            return False

    return True


if __name__ == '__main__':
    valid_tree = ET.parse('./period_checker/sample_period.xml')
    invalid_tree = ET.parse('./period_checker/wrong_period.xml')
    print(valid_period(valid_tree))
    print(valid_period(invalid_tree))
