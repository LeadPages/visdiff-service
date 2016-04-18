*** Settings ***
Library    Selenium2Library
Test Teardown    Close Browser


*** Test Cases ***
Record Base Images
    # start with main www.leadpages.net page
    Open Browser    https://www.leadpages.net/    browser=chrome
    Wait Until Element Is Visible    id=bgvid
    Execute Javascript    document.querySelector('#bgvid').pause(); document.querySelector('#bgvid').currentTime = 0;
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=www_leadpages/www_leadpages_baseline.png
    # get pricing page
    Go To   https://www.leadpages.net/pricing
    Sleep    1
    Capture Page Screenshot    filename=www_leadpages_pricing/www_leadpages_pricing_baseline.png
    # get library page
    Go To   https://www.leadpages.net/library
    Sleep    1
    Capture Page Screenshot    filename=www_leadpages_library/www_leadpages_library_baseline.png
    # get blog page
    Go To   https://blog.leadpages.net/
    Sleep    1
    Capture Page Screenshot    filename=blog_leadpages/blog_leadpages_baseline.png

