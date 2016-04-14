*** Settings ***
Library    pdiff.py
Library    Selenium2Library
Test Teardown    Close Browser


*** Test Cases ***
#Record Base Images
#    Open Browser    https://my.leadpagestest.net    browser=chrome
#    Wait Until Element Is Enabled    id=lego-login-submit
#    Set Window Size    ${375}    ${669}
#    Sleep    1
#    Capture Page Screenshot    filename=test_small_real.png
#    Set Window Size    ${715}    ${837}
#    Sleep    1
#    Capture Page Screenshot    filename=test_med_real.png
#    Set Window Size    ${1193}    ${805}
#    Sleep    1
#    Capture Page Screenshot    filename=test_large_real.png
#    Set Window Size    ${2200}    ${1800}
#    Sleep    1
#    Capture Page Screenshot    filename=test_xl_real.png
#    Input Text                       css=[name="username"]        justin.betz+testenterprise@ave81.com
#    Input Password                   css=[name="password"]        ocecotase
#    Click Button                     css=[name="form-submit"]
#    Wait Until Element Is Enabled    name=create-page-button
#    Set Window Size    ${375}    ${669}
#    Sleep    1
#    Capture Page Screenshot    filename=test_small_mypages_real.png
#    Set Window Size    ${715}    ${837}
#    Sleep    1
#    Capture Page Screenshot    filename=test_med_mypages_real.png
#    Set Window Size    ${1193}    ${805}
#    Sleep    1
#    Capture Page Screenshot    filename=test_large_mypages_real.png
#    Set Window Size    ${2200}    ${1800}
#    Sleep    1
#    Capture Page Screenshot    filename=test_xl_mypages_real.png

Check Size Of Login
    Open Browser    https://my.leadpagestest.net    browser=chrome
    Wait Until Element Is Enabled    id=lego-login-submit
    Set Window Size    ${375}    ${669}
    Sleep    1
    Capture Page Screenshot    filename=test_small.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_small.png    test_small_real.png
    Should Be True    ${diff_percent} < 2.0    Small viewport differed from baseline by more than 2%
#    Go To    http://the-internet.herokuapp.com/abtest
    Set Window Size    ${715}    ${837}
    Sleep    1
    Capture Page Screenshot    filename=test_med.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_med.png    test_med_real.png
    Should Be True    ${diff_percent} < 2.0   Medium viewport differed from baseline by more than 2%
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=test_large.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_large.png    test_large_real.png
    Should Be True    ${diff_percent} < 2.0    Large viewport differed from baseline by more than 2%
    Set Window Size    ${2200}    ${1800}
    Sleep    1
    Capture Page Screenshot    filename=test_xl.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_xl.png    test_xl_real.png
    Should Be True    ${diff_percent} < 2.0    XL viewport differed from baseline by more than 2%

Check Size Of MyPages
    Open Browser    https://my.leadpagestest.net    browser=chrome
    Wait Until Element Is Enabled    id=lego-login-submit
    Input Text                       css=[name="username"]        justin.betz+testenterprise@ave81.com
    Input Password                   css=[name="password"]        ocecotase
    Click Button                     css=[name="form-submit"]
    Wait Until Element Is Enabled    name=create-page-button
    Set Window Size    ${375}    ${669}
    Sleep    1
    Capture Page Screenshot    filename=test_mypages_small.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_mypages_small.png    test_small_mypages_real.png
    Should Be True    ${diff_percent} < 2.0    Small viewport differed from baseline by more than 2%
    Set Window Size    ${715}    ${837}
    Sleep    1
    Capture Page Screenshot    filename=test_mypages_med.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_mypages_med.png    test_med_mypages_real.png
    Should Be True    ${diff_percent} < 2.0   Medium viewport differed from baseline by more than 2%
    Set Window Size    ${1193}    ${805}
    Sleep    1
    Capture Page Screenshot    filename=test_mypages_large.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_mypages_large.png    test_large_mypages_real.png
    Should Be True    ${diff_percent} < 2.0    Large viewport differed from baseline by more than 2%
    Set Window Size    ${2200}    ${1800}
    Sleep    1
    Capture Page Screenshot    filename=test_mypages_xl.png
    ${diff_count}    ${diff_percent} =    gen p diff    test_mypages_xl.png    test_xl_mypages_real.png
    Should Be True    ${diff_percent} < 2.0    XL viewport differed from baseline by more than 2%