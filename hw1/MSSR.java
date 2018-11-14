/*
 * Assignment 1
 * Name: 潘闻兮
 * Student ID: 1709853X-I011-0010
 *
 * Description:
 *  Read input, store the records in an array of Student class
 *  Ask user to choose field to be sorted and sorting way
 *  Sort by ascending way or descending way
 *
 * Contain:
 *  class Student
 *  abstract class Sort
 *  class ASort
 *  class DSort
 *  class MSSR
 */


class Student {
    private String studentID;
    private String studentName;
    private String courseCode;
    private String score;
    private String field;

    Student(String studentID, String studentName, String courseCode, String score)
    {
      this.studentID = studentID;
      this.studentName = studentName;
      this.courseCode = courseCode;
      this.score = score;
    }

    public String getStudentID() {
        return studentID;
    }

    public String getStudentName() {
        return studentName;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public String getScore() {
        return score;
    }

    public void setField(int field)
    {
        switch (field)
        {
            case 1:
                this.field = studentID;
                break;
            case 2:
                this.field = studentName;
                break;
            case 3:
                this.field = courseCode;
                break;
            case 4:
                this.field = score;
                break;
        }
    }

    public String getField() {
        return field;
    }
}


abstract class Sort{
    private Student[] students;

    Sort(Student[] students) {
        this.students = students;
    }

    public void display()
    {
        //display the sorting result

        for (Student student : students)
        {
            StdOut.printf("%s,%s,%s,%s\n",
                    student.getStudentID(),
                    student.getStudentName(),
                    student.getCourseCode(),
                    student.getScore());
        }
    }

    private void exch(int i, int j)
    {
        Student t = students[i];
        students[i] = students[j];
        students[j] = t;
    }

    abstract boolean compare(String v, String w);

    private int partition(int lo, int hi)
    {
        int i = lo, j = hi + 1;
        String v = students[lo].getField();
        while(true)
        {
            while(compare(students[++i].getField(), v)) if(i == hi) break;
            while(compare(v, students[--j].getField())) if(j == lo) break;
            if(i >= j) break;
            exch(i, j);  //exchange students[i] and students[j]
        }
        exch(lo, j);
        return j;
    }

    public void sort(int lo, int hi)
    {
        if(hi <= lo)
            return;
        int j = partition(lo, hi);
        sort(lo, j-1);  //left sort
        sort(j+1, hi);  //right sort
    }
}


class ASort extends Sort
{
    //Ascending way
    ASort(Student[] students) {
        super(students);
    }

    public boolean compare(String v, String w)
    {
        return v.compareTo(w) < 0;  //v < w
    }
}


class DSort extends Sort
{
    //Descending way
    DSort(Student[] students) {
        super(students);
    }

    public boolean compare(String v, String w)
    {
        return w.compareTo(v) < 0;  //w < v
    }
}


public class MSSR {
    public static void main(String[] args)
    {
        int N = Integer.parseInt(StdIn.readLine());  //number of students
        Student[] students = new Student[N];

        int i;
        //store records of students
        for (i = 0; i < N; ++i)
        {
            String line = StdIn.readLine();
            String[] record = line.split(",");
            students[i] = new Student(record[0], record[1], record[2], record[3]);
        }

        Queue<String> queue = new Queue<>();
        while (true)
        {
            //input field and way
            String option = StdIn.readLine();
            if (option.equals("0"))
                break;
            queue.enqueue(option);
        }
        while (!queue.isEmpty())
        {
            StdRandom.shuffle(students);  //shuffle students
            String[] option = queue.dequeue().split(" ");
            int field = Integer.parseInt(option[0]);
            char way = option[1].charAt(0);

            for (i = 0; i < N; ++i)
                students[i].setField(field);
            //sort
            switch (way)
            {
                case 'A':
                    //Ascending
                    ASort aSort = new ASort(students);
                    aSort.sort(0, N-1);
                    aSort.display();
                    break;
                case 'D':
                    //Descending
                    DSort dSort = new DSort(students);
                    dSort.sort(0, N-1);
                    dSort.display();
                    break;
            }
            if (!queue.isEmpty())
                StdOut.println();
        }

    }
}
