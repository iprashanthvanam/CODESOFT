import java.util.Scanner;

public class GradeCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input number of subjects
        System.out.print("Enter the number of subjects: ");
        int numSubjects;
        try {
            numSubjects = Integer.parseInt(scanner.nextLine());
            if (numSubjects <= 0) {
                System.out.println("Number of subjects must be positive!");
                scanner.close();
                return;
            }
        } catch (NumberFormatException e) {
            System.out.println("Please enter a valid number!");
            scanner.close();
            return;
        }

        // Array to store marks
        double[] marks = new double[numSubjects];
        double totalMarks = 0;

        // Input marks for each subject
        for (int i = 0; i < numSubjects; i++) {
            System.out.print("Enter marks for subject " + (i + 1) + " (out of 100): ");
            try {
                double mark = Double.parseDouble(scanner.nextLine());
                if (mark < 0 || mark > 100) {
                    System.out.println("Marks must be between 0 and 100!");
                    i--; // Retry for this subject
                    continue;
                }
                marks[i] = mark;
                totalMarks += mark;
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number!");
                i--; // Retry for this subject
            }
        }

        // Calculate average percentage
        double averagePercentage = totalMarks / numSubjects;

        // Determine grade
        String grade = calculateGrade(averagePercentage);

        // Display results
        System.out.println("\n--- Results ---");
        System.out.printf("Total Marks: %.2f out of %d%n", totalMarks, numSubjects * 100);
        System.out.printf("Average Percentage: %.2f%%%n", averagePercentage);
        System.out.println("Grade: " + grade);

        scanner.close();
    }

    // Method to calculate grade based on average percentage
    private static String calculateGrade(double percentage) {
        if (percentage >= 90) {
            return "A+";
        } else if (percentage >= 80) {
            return "A";
        } else if (percentage >= 70) {
            return "B";
        } else if (percentage >= 60) {
            return "C";
        } else if (percentage >= 50) {
            return "D";
        } else {
            return "F";
        }
    }
}