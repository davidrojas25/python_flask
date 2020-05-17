from warriors import db, Runners, Coach, Run



db.create_all()
#creating 2 runners
Ariel = Runners('Ariel', 'Salinas', '11', 'Jaguar')
Jay = Runners('Jay', 'Lopez', '9', 'Eagle')

#add runners to DB
db.session.add_all([Ariel, Jay])
db.session.commit()

#check
print(Runners.query.all())

Ariel = Runners.query.filter_by(firstname='Ariel').first()
print(Ariel)

# create coach
David = Coach('David', Ariel.id)

# create runs
run1 = Run('around lake', Ariel.id)
run2 = Run('on the track', Ariel.id)

db.session.add_all([David, run1, run2])
db.session.commit()

#grab Ariel after adds
Ariel = Runners.query.filter_by(firstname='Ariel').first()
print(Ariel)
# print the report
Ariel.report_runs()
