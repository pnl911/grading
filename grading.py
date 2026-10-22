import pandas as pd



df = pd.read_csv('553_grade.csv')
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

students = df.loc[
    ~df['Student'].astype(str).str.contains('Points Possible', case=False, na=False)
].copy()
top_n = max(1, (len(students) + 9) // 10)
cutoff = students['grade_man'].nlargest(top_n).min()
top_students = (
    students.loc[students['grade_man'] >= cutoff]
    .sort_values('grade_man', ascending=False)[['Student', 'SIS Login ID']]
)
print('Top 10% by total points:')
print(top_students.to_string(index=False))
top_students.to_csv('553_top_10_percent_students.csv', index=False)

df.to_csv('553_letter.csv',index=False)