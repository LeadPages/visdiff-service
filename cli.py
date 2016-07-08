import sys
from app import image_diff
import base64


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Please specify both ImageA and ImageB and a difference " \
            " threshold (suggested: 40)\n >python pdiff.py <ImageA> <ImageB>" \
            "<threshold>\n"
        sys.exit("Wrong number of arguments")

    report = image_diff.generate_difference_report(sys.argv[1], sys.argv[2],
                                                   True)

    print "Detected %d different pixels, %f percent difference\n" \
        % (report['diffCount'], report['diffPercent'])

    with open('diff2.png', 'wb') as file:
        file.write(base64.b64decode(report['outputImage']))
