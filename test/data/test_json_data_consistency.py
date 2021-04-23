def test_entry_exist_across_all_jsons():
    import json
    with open('data/characters.json', 'r') as charFile, open('data/ougi.json', 'r') as ougiFile, open('data/supportskill.json', 'r') as supportFile, \
        open('data/skill.json', 'r') as skillFile, open('data/emp.json', 'r') as empFile:
        characters = json.load(charFile)
        ougis = json.load(ougiFile)
        supports = json.load(supportFile)
        skills = json.load(skillFile)
        emps = json.load(empFile)
    
    for character in characters:
        assert character in ougis, f'Character {character} not found in ougi'
        assert character in supports, f'Character {character} not found in support skill'
        assert character in skills, f'Character {character} not found in skill'
        assert character in emps, f'Character {character} not found in emp'
        print(f'Test Character {character} - PASSED')
        for version in characters[character]:
            assert version in ougis[character], f'Version {version} not found for character {character} in ougi'
            assert version in supports[character], f'Version {version} not found for character {character} in support skill'
            assert version in skills[character], f'Version {version} not found for character {character} in skill'
            assert version in emps[character], f'Version {version} not found for character {character} in emp'
            print(f'Test version {version} of character {character} - PASSED')