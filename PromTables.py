import copy
print("\033c")

### https://docs.google.com/spreadsheets/d/14QvgWvUbX0FI90EFg95FI9NPYc4f37FqrGQY8CWjGuA/edit?usp=sharing # UCTech, Magnet, APA, Allied ###
### https://docs.google.com/spreadsheets/d/19bIABPB_IcS2PR_Cjz2ly7mXjmEe3Mlayabs9fIgpaI/edit?usp=sharing # AIT ###

all = []
groups = []
group = []

# Read input and break into groups
with open('input.txt') as fI:
	for line in fI.readlines():
		line = line.strip("\n").replace(":","-").strip().title()
		all.append(line.strip("\"").split("-")[0].strip())

		if line.endswith("\""):
			group.append(line.strip("\"").split("-")[0].strip())
			groups.append(group)
			group = []
		else:
			group.append(line.strip("\"").split("-")[0].strip())

# Label by size
for group in groups:
	for p in group[1:]:
		if p.strip() == "":
			group.remove(p)
	group.insert(0,len(group))

# Organize by size
groups.sort(key=lambda x: x[0],reverse=True)

print("Initial Groups:")
for group in groups:
	print(group,"\n")

# Create tables
try:
	count = 1
	removed = 0	
	fO = open('tables.txt','w')

	for i in range(len(groups)):
		# If a table has already been made by a group
		if groups[i-removed][0] == 12:
			fO.write(f"\nTable {count}:\n")
			c = 1
			for p in groups[i-removed][1:]:
				fO.write(f"{c}) {p}\n")
				c += 1
			groups.pop(i-removed)
			removed += 1
			count += 1
		# Combines Two Tables
		elif groups[i-removed][0] > 5:
			revGroups = sorted(groups, key=lambda x: x[0])
			revGroups2 = sorted(groups, key=lambda x: x[0])
			for j in range(len(revGroups)):
				n = 12 - groups[i-removed][0]
				if revGroups[j][0] == n and revGroups[j][1] != groups[i-removed][1]:
					fO.write(f"\nTable {count}:\n")
					c = 1
					for p in groups[i-removed][1:]:
						fO.write(f"{c}) {p}\n")
						c += 1
					groups.pop(i-removed)
					for p in revGroups[j][1:]:
						fO.write(f"{c}*) {p}\n")
						c += 1
					groups.pop(groups.index(revGroups[j]))
					removed += 1
					count += 1
		else:
			n = 12 - groups[i-removed][0]
			groups1 = copy.copy(groups)
			groups2 = copy.copy(groups)
			for j in range(len(groups)):
				if groups1[j][0] < n and groups1[j][1] != groups[i-removed][1]:
					n -= groups1[j][0]
					for k in range(len(groups2)):
						if groups2[k][0] == n and groups1[j][1] != groups[i-removed][1] and groups1[j][1] != groups2[k][1] and groups2[k][1] != groups[i-removed][1]:
							fO.write(f"\nTable {count}:\n")
							c = 1
							for p in groups[i-removed][1:]:
								fO.write(f"{c}) {p}\n")
								c += 1
							groups.pop(i-removed)
							for p in groups1[j][1:]:
								fO.write(f"{c}*) {p}\n")
								c += 1
							for p in groups2[k][1:]:
								fO.write(f"{c}) {p}\n")
								c += 1
							groups.pop(groups.index(groups1[j]))
							groups.pop(groups.index(groups2[k]))
							removed += 2
							count += 1	
except:
	fO.close()

# Remaining groups that were not assigned a table
with open('leftover.txt','w') as fL:
	for i in range(len(groups)):
		fL.write(f"\nGroup {i+1} (Size = {groups[i][0]})")
		str = ", ".join(groups[i][1:])
		fL.write(f"\n[{str}]\n")

all.sort()
print(all)
with open('all.txt','w') as fA:
	for person in all:
		fA.write(f"{person}\n")
