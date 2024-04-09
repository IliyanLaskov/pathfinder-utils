import json
import shutil


def abconvert(ability):
    return 10 + ability * 2


def parseskills():
    skills = ["acrobatics", "arcana", "athletics", "crafting", "deception", "diplomacy", "intimidation", "medicine",
              "nature", "occultism", "performance", "religion", "society", "stealth", "survival", "thievery"]
    parsed = []
    for skill in skills:
        if sourceCreature[skill]['value'] != "":
            parsed.append({"Name": skill, "Modifier": sourceCreature[skill]['value']})
    return parsed


def parsestrikes():
    actions = []
    meleecontent = ""
    rangedcontent = ""
    for strike in sourceCreature['strikes']:
        if strike['type'] == "Melee":
            meleecontent = f'{meleecontent}{strike["name"]} +{str(strike["attack"])}'
            if strike['traits'] != "":
                meleecontent = f'{meleecontent} ({strike['traits']})'
            meleecontent = f'{meleecontent}, Damage {strike["damage"]}\n'

        if strike['type'] == "Ranged":
            rangedcontent = f'{strike["name"]} +{strike["attack"]}'
            if strike['traits'] != "":
                rangedcontent = f'{rangedcontent} ({strike['traits']})'
            rangedcontent = f'{rangedcontent}, Damage {strike["damage"]}\n'
    if meleecontent != "":
        actions.append({"Name": "Melee", "Content": meleecontent})
    if rangedcontent != "":
        actions.append({"Name": "Ranged", "Content": rangedcontent})
    return actions


def parsespecialactions():
    actions = []
    for special in sourceCreature['specials']:
        if special['actions'] != "none":
            description = f'{special['actions']} action(s)\n{special["description"]}'
            actions.append({"Name": special['name'], "Content": description})
    return actions


def parsespecialactiontraits():
    traits = []
    for special in sourceCreature['specials']:
        if special['actions'] == "none":
            traits.append({"Name": special['name'], "Content": special["description"]})
    return traits


def parseaction():
    return parsestrikes() + parsespecialactions()

shutil.copyfile("ii-creature-template.json", "new_creature.json")

# read file
with open('KoboldWarrior.pf2.tools.json', 'r') as file:
    source = file.read()
sourceCreature = json.loads(source)

with open('new_creature.json', 'r') as file:
    new = file.read()
newCreature = json.loads(new)

# parse description
newCreature['Creatures.bvuzfgt2']['Name'] = sourceCreature['name']
newCreature['Creatures.bvuzfgt2']['InitiativeModifier'] = sourceCreature['perception']['value']
newCreature['Creatures.bvuzfgt2']['Senses'] = [sourceCreature['perception']['note']]
newCreature['Creatures.bvuzfgt2']['Languages'] = [sourceCreature['languages']]
newCreature['Creatures.bvuzfgt2']['Skills'] = parseskills()
newCreature['Creatures.bvuzfgt2']['Traits'] = parsespecialactiontraits()

# parse combat stats
newCreature['Creatures.bvuzfgt2']['HP']['Value'] = sourceCreature['hp']['value']
newCreature['Creatures.bvuzfgt2']['AC']['Value'] = sourceCreature['ac']['value']
newCreature['Creatures.bvuzfgt2']['Speed'] = [sourceCreature['speed']]
newCreature['Creatures.bvuzfgt2']['Saves'] = [
    {"Name": "Fort", "Modifier": sourceCreature['fortitude']['value']},
    {"Name": "Ref", "Modifier": sourceCreature['reflex']['value']},
    {"Name": "Will", "Modifier": sourceCreature['will']['value']}
]
newCreature['Creatures.bvuzfgt2']['Actions'] = parseaction()

# parse attribute scores
newCreature['Creatures.bvuzfgt2']['Abilities']['Str'] = abconvert(sourceCreature['strength']['value'])
newCreature['Creatures.bvuzfgt2']['Abilities']['Dex'] = abconvert(sourceCreature['dexterity']['value'])
newCreature['Creatures.bvuzfgt2']['Abilities']['Con'] = abconvert(sourceCreature['constitution']['value'])
newCreature['Creatures.bvuzfgt2']['Abilities']['Int'] = abconvert(sourceCreature['intelligence']['value'])
newCreature['Creatures.bvuzfgt2']['Abilities']['Wis'] = abconvert(sourceCreature['wisdom']['value'])
newCreature['Creatures.bvuzfgt2']['Abilities']['Cha'] = abconvert(sourceCreature['charisma']['value'])

with open('new_creature.json', 'w') as file:
    json.dump(newCreature, file)
