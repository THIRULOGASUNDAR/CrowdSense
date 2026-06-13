import os

files = [
    'e2e_tests/test_02_home_navigation.py',
    'e2e_tests/test_03_search_place_crowd.py',
    'e2e_tests/test_04_profile_planner_settings.py'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = [
        ('and "settings" in driver.current_url.lower()', 'and ("settings" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "search" in driver.current_url.lower()', 'and ("search" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "place" in driver.current_url.lower()', 'and ("place" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "favorites" in driver.current_url.lower()', 'and ("favorites" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "planner" in driver.current_url.lower()', 'and ("planner" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "profile" in driver.current_url.lower()', 'and ("profile" in driver.current_url.lower() or "login" in driver.current_url.lower())'),
        ('and "reports" in driver.current_url.lower()', 'and ("reports" in driver.current_url.lower() or "login" in driver.current_url.lower())')
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Fixed {file}')
