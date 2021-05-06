def test_entry_exist_across_all_jsons():
    import json
    from urllib.request import urlopen
    dataPath = "https://raw.githubusercontent.com/nnguyen259/KoluluData/master"
    
    characters = json.load(urlopen(f'{dataPath}/characters.json'))
    ougis = json.load(urlopen(f'{dataPath}/ougi.json'))
    supports = json.load(urlopen(f'{dataPath}/supportskill.json'))
    skills = json.load(urlopen(f'{dataPath}/skill.json'))
    emps = json.load(urlopen(f'{dataPath}/emp.json'))
    
    for character in characters:
        assert character in ougis, f'Character {character} not found in ougi'
        assert character in supports, f'Character {character} not found in support skill'
        assert character in skills, f'Character {character} not found in skill'
        assert character in emps, f'Character {character} not found in emp'
        for version in characters[character]:
            if '_' in version:
                assert version[:-2] in characters[character], f'Version {version} exists without base for character {character}'
            assert version in ougis[character], f'Version {version} not found for character {character} in ougi'
            assert version in supports[character], f'Version {version} not found for character {character} in support skill'
            assert version in skills[character], f'Version {version} not found for character {character} in skill'
            assert version in emps[character], f'Version {version} not found for character {character} in emp'