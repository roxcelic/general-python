from dic import elements
elements_keys = list(elements.keys())
print("What word would you like to try and find in the periodic table?")
searchtm = input(" - ").replace(" ", "").lower()
used = []
def can_construct_term(term, element_list):
    el = ""
    if not term:
        return True
    for element in element_list:
        if term.startswith(element.lower()):
            if len(el) < len(element): el = element
    if el:
        remaining_term = term[len(el):]
        used.append(el)
        if can_construct_term(remaining_term, element_list):
            return True
    return False
if can_construct_term(searchtm, elements_keys):
    print(f"{searchtm} can be made using the following elements: ")
    for item in used: print(f"{item} :  {elements[item]}")
elif used:
    print(f"{searchtm} cannot be made but here is the closet: \n{''.join(used).lower()}")
    for item in used: print(f"{item} :  {elements[item]}")
else: print(f"{searchtm} cannot even be started")