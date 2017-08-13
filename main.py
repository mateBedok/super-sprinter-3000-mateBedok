from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_list():
    stories = read_data('database.csv')
    if request.method == "POST":
        return add_new_story()
    else:
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')

@app.route('/story', methods=['POST'])
def add_new_story():
    return render_template('form.html', title='Add new Story', button='Create', story=['', '', '', '', '', '', ''])


@app.route('/list', methods=['POST'])
def Edit():
    stories = read_data('database.csv')
    if request.form['button'] == 'Create':
        if len(stories) == 1:
            id_number = '1'
        else:
            id_number = str(int(stories[len(stories)-1][0])+1)
        new_row = []
        new_row.append(id_number)
        new_row.append(request.form['story_title'])
        new_row.append(request.form['user_story'])
        new_row.append(request.form['criteria'])
        new_row.append(request.form['value'])
        new_row.append(request.form['estimation'])
        new_row.append(request.form['status'])
        stories = append_data(new_row)
        return render_template('list.html', stories=stories, title='Super Sprinter 3000')
    elif request.form['button'] == 'Edit':
        original_data = read_data()
        id = request.form['id']
        edit_row = []
        edit_row.append(id)
        edit_row.append(request.form['story_title'])
        edit_row.append(request.form['user_story'])
        edit_row.append(request.form['criteria'])
        edit_row.append(request.form['value'])
        edit_row.append(request.form['estimation'])
        edit_row.append(request.form['status'])
        new_data = []
        for row in original_data:
            if row[0] != id:
                new_data.append(row)
            else:
                new_data.append(edit_row)
        write_data(new_data)
        return redirect('/')


@app.route('/edit/<id>')
def edit(id):
    stories = read_data()
    for row in stories:
        if row[0] == id:
            story = row
    return render_template('form.html', title='Edit Story', button='Edit', story=story, id=id)


@app.route('/delete/<id>')
def remove(id):
    original_data = read_data()
    new_data = []
    for number, row in enumerate(original_data):
        if row[0] != id:
            new_data.append(row)
        if row[0] != 1 and number == 1:
            row[0] = '1'
        elif number > 1:
            row[0] = number -1
    write_data(new_data)
    return redirect('/')


def read_data(file_name='database.csv'):
    data = []
    with open(file_name, newline='') as file:
            datareader = csv.reader(file, delimiter=',', quotechar='|')
            for row in datareader:
                data.append(row)
    return data


def append_data(new_story, file_name='database.csv'):
    with open(file_name, 'a', newline='') as file:
        datawriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(new_story)
    stories = read_data('database.csv')
    return stories


def write_data(story, file_name='database.csv'):
    with open(file_name, 'w', newline='') as file:
        datawriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(story)


if __name__ == '__main__':
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
