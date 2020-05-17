from warriors import db, Runners

db.create_all()

victoria =  Runners('Victoria', 'Ruiz', 13)
lola = Runners('Lola', 'Esparza', 12)
# should yield none
print(victoria.id)
print(lola.id)

# to add all items to db
db.session.add_all([victoria, lola])
#to add one at a time
#db.session.add(victoria)
#db.session.add(lola)

db.session.commit()

print(victoria.id)
print(lola.id)