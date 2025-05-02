import xml.etree.ElementTree as ET


def valid_period(period: ET.ElementTree) -> bool:
    root = period.getroot()
    start = root.attrib.get('start')
    if not start:
        print('Invalid Period, no start found')
        return False

    # check adaptationset
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

    print(f'Valid Tree')
    return True


if __name__ == '__main__':
    valid_tree = ET.parse('./period_checker/valid_period.xml')
    valid_period(valid_tree)

    invalid_tree_no_start = ET.parse('./period_checker/invalid_period_no_start.xml')
    invalid_tree_no_adapt = ET.parse('./period_checker/invalid_period_no_adaptationset.xml')
    invalid_tree_no_rep = ET.parse('./period_checker/invalid_period_no_representation.xml')
    invalid_tree_no_segment = ET.parse('./period_checker/invalid_period_no_segment.xml')
    invalid_tree_no_media = ET.parse('./period_checker/invalid_period_no_media.xml')
    invalid_tree_bad_format = ET.parse('./period_checker/invalid_period_bad_format.xml')
    invalid_tree_no_init = ET.parse('./period_checker/invalid_period_no_init.xml')

    valid_period(invalid_tree_no_start)
    valid_period(invalid_tree_no_adapt)
    valid_period(invalid_tree_no_rep)
    valid_period(invalid_tree_no_segment)
    valid_period(invalid_tree_no_media)
    valid_period(invalid_tree_bad_format)
    valid_period(invalid_tree_no_init)
