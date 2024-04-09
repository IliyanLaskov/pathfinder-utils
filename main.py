import json
import shutil
import random


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
with open('GiantRat1712692659.json', 'r') as file:
    source = file.read()
sourceCreature = json.loads(source)

with open('new_creature.json', 'r') as file:
    new = file.read()
newCreature = json.loads(new)

rid = str(random.randrange(10000000, 99999999))
newid = f'Creatures.{rid}'

newCreature[newid] = newCreature['Creatures.templateID']
newCreature.pop('Creatures.templateID')
newCreature['Creatures'] = [rid]

# parse description
newCreature[newid]['Id'] = rid
newCreature[newid]['Name'] = sourceCreature['name']
newCreature[newid]['InitiativeModifier'] = sourceCreature['perception']['value']
newCreature[newid]['Senses'] = [sourceCreature['perception']['note']]
if 'languages' in sourceCreature:
    newCreature[newid]['Languages'] = [sourceCreature['languages']]
newCreature[newid]['Skills'] = parseskills()
newCreature[newid]['Traits'] = parsespecialactiontraits()

# parse combat stats
newCreature[newid]['HP']['Value'] = sourceCreature['hp']['value']
newCreature[newid]['AC']['Value'] = sourceCreature['ac']['value']
newCreature[newid]['Speed'] = [sourceCreature['speed']]
newCreature[newid]['Saves'] = [
    {"Name": "Fort", "Modifier": sourceCreature['fortitude']['value']},
    {"Name": "Ref", "Modifier": sourceCreature['reflex']['value']},
    {"Name": "Will", "Modifier": sourceCreature['will']['value']}
]
newCreature[newid]['Actions'] = parseaction()

# parse attribute scores
newCreature[newid]['Abilities']['Str'] = abconvert(sourceCreature['strength']['value'])
newCreature[newid]['Abilities']['Dex'] = abconvert(sourceCreature['dexterity']['value'])
newCreature[newid]['Abilities']['Con'] = abconvert(sourceCreature['constitution']['value'])
newCreature[newid]['Abilities']['Int'] = abconvert(sourceCreature['intelligence']['value'])
newCreature[newid]['Abilities']['Wis'] = abconvert(sourceCreature['wisdom']['value'])
newCreature[newid]['Abilities']['Cha'] = abconvert(sourceCreature['charisma']['value'])

with open('new_creature.json', 'w') as file:
    json.dump(newCreature, file)
