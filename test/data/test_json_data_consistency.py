def test_entry_exist_across_all_jsons():
    import json
    with open('data/characters.json', 'r') as charFile, open('data/ougi.json', 'r') as ougiFile, open('data/supportskill.json', 'r') as supportFile:
        characters = json.load(charFile)
        ougis = json.load(ougiFile)
        supports = json.load(supportFile)
    
    for character in characters:
        assert ougis[character] and supports[character]
        print(f'Test Character {character} - PASSED')
        for version in characters[character]:
            assert ougis[character][version] and supports[character][version]
            print(f'Test version {version} of character {character} - PASSED')