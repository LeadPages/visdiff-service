*** Settings ***
Library    pdiff.py
Library    Selenium2Library
Library    OperatingSystem
Test Teardown    Close Browser


*** Test Cases ***
Validate That The Blog Is Ok
    Open Browser    https://blog.leadpages.net/    browser=chrome
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=blog_test.png
    @{baseline_images} =    List Files In Directory    ./blog_leadpages
    : FOR    ${baseline_image}    IN    @{baseline_images}
    \    ${diff_count}    ${diff_percent} =    gen p diff    blog_test.png    blog_leadpages/${baseline_image}
    \    ${status}    ${return} =    Run Keyword And Ignore Error    Should Be True    ${diff_percent} < 2.0
    \    Run Keyword If    '${status}' == 'PASS'    Exit For Loop
    Run Keyword If    '${status}' != 'PASS'    Fail    Check https://blog.leadpages.net/ it failed to match the baseline screenshot!

Validate That The Main Page Is Ok
    Open Browser    https://www.leadpages.net/    browser=chrome
    Wait Until Element Is Visible    id=bgvid
    Execute Javascript    document.querySelector('#bgvid').pause(); document.querySelector('#bgvid').currentTime = 0;
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=leadpages_test.png
    @{baseline_images} =    List Files In Directory    ./www_leadpages
    : FOR    ${baseline_image}    IN    @{baseline_images}
    \    ${diff_count}    ${diff_percent} =    gen p diff    leadpages_test.png    www_leadpages/${baseline_image}
    \    ${status}    ${return} =    Run Keyword And Ignore Error    Should Be True    ${diff_percent} < 2.0
    \    Run Keyword If    '${status}' == 'PASS'    Exit For Loop
    Run Keyword If    '${status}' != 'PASS'    Fail    Check https://www.leadpages.net/ it failed to match the baseline screenshot!

Validate That The Library Is Ok
    Open Browser    https://www.leadpages.net/library    browser=chrome
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=library_test.png
    @{baseline_images} =    List Files In Directory    ./www_leadpages_library
    : FOR    ${baseline_image}    IN    @{baseline_images}
    \    ${diff_count}    ${diff_percent} =    gen p diff    library_test.png    www_leadpages_library/${baseline_image}
    \    ${status}    ${return} =    Run Keyword And Ignore Error    Should Be True    ${diff_percent} < 2.0
    \    Run Keyword If    '${status}' == 'PASS'    Exit For Loop
    Run Keyword If    '${status}' != 'PASS'    Fail    Check https://www.leadpages.net/library it failed to match the baseline screenshot!

Validate That The Pricing Page Is Ok
    Open Browser    https://www.leadpages.net/pricing    browser=chrome
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=pricing_test.png
    @{baseline_images} =    List Files In Directory    ./www_leadpages_pricing
    : FOR    ${baseline_image}    IN    @{baseline_images}
    \    ${diff_count}    ${diff_percent} =    gen p diff    pricing_test.png    www_leadpages_pricing/${baseline_image}
    \    ${status}    ${return} =    Run Keyword And Ignore Error    Should Be True    ${diff_percent} < 2.0
    \    Run Keyword If    '${status}' == 'PASS'    Exit For Loop
    Run Keyword If    '${status}' != 'PASS'    Fail    Check https://www.leadpages.net/pricing it failed to match the baseline screenshot!
