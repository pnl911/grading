import pandas as pd



df = pd.read_csv('551_grade.csv')
print(df.head(5))

assignment_end = df.columns.get_loc('Assignments Current Points')
score_columns = [
    column for column in df.columns[4:assignment_end]
    if not column.startswith(('Roll Call Attendance', 'For Instructor Use Only'))
]
df['grade_man'] = (
    df[score_columns]
    .apply(pd.to_numeric, errors='coerce')
    .sum(axis=1)
)
percentage = round(df['grade_man'] / 300 * 100, 0)
df['percentage'] = percentage
print(df.head(5))

df['grade_letter'] = percentage.apply(
    lambda x: (
        'A+' if x >= 97
        else 'A' if x >= 93
        else 'A-' if x >= 90
        else 'B+' if x >= 87
        else 'B' if x >= 83
        else 'B-' if x >= 80
        else 'C+' if x >= 77
        else 'C' if x >= 73
        else 'C-' if x >= 70
        else 'D+' if x >= 67
        else 'D' if x >= 63
        else 'D-' if x >= 60
        else 'F'
    )
)

df.to_csv('551.csv',index=False)