from warriors import db, Runners

## create example
my_runner = Runners('Gabriel', 'Barajas', 9)
db.session.add(my_runner)
db.session.commit()

## read example
all_runners = Runners.query.all()
print(all_runners)

## select by ID
runner_one = Runners.query.get(1)
print(runner_one.firstname)

#filter example
runner_lola = Runners.query.filter_by(firstname='Lola')
print(runner_lola.all())


##### Update
first_runner = Runners.query.get(1)
first_runner.age = 12
db.session.add(first_runner)
db.session.commit()

###check for changes
all_runners = Runners.query.all()
print(all_runners)