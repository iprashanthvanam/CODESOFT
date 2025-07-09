import java.util.Random;
import java.util.Scanner;

public class NumberGame {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        boolean playAgain = true;
        int totalScore = 0;
        int roundsPlayed = 0;

        while (playAgain) {
            int minRange = 1;
            int maxRange = 100;
            int maxAttempts = 7;
            int attempts = 0;
            int score = 0;

            // Generate random number
            int targetNumber = random.nextInt(maxRange - minRange + 1) + minRange;
            System.out.println("\nNew Round! I'm thinking of a number between " + minRange + " and " + maxRange);
            System.out.println("You have " + maxAttempts + " attempts to guess it!");

            // Game loop for one round
            while (attempts < maxAttempts) {
                System.out.print("Enter your guess: ");
                int guess;
                
                // Input validation
                try {
                    guess = Integer.parseInt(scanner.nextLine());
                } catch (NumberFormatException e) {
                    System.out.println("Please enter a valid number!");
                    continue;
                }

                attempts++;
                
                // Compare guess with target
                if (guess == targetNumber) {
                    score = calculateScore(attempts, maxAttempts);
                    totalScore += score;
                    roundsPlayed++;
                    System.out.println("Congratulations! You guessed the number in " + attempts + " attempts!");
                    System.out.println("Round score: " + score);
                    break;
                } else if (guess < targetNumber) {
                    System.out.println("Too low! Attempts left: " + (maxAttempts - attempts));
                } else {
                    System.out.println("Too high! Attempts left: " + (maxAttempts - attempts));
                }

                // Check if attempts are exhausted
                if (attempts == maxAttempts) {
                    System.out.println("Game Over! The number was: " + targetNumber);
                    roundsPlayed++;
                }
            }

            // Display current stats
            System.out.println("\nCurrent Stats:");
            System.out.println("Rounds played: " + roundsPlayed);
            System.out.println("Total score: " + totalScore);

            // Ask to play again
            System.out.print("\nWould you like to play another round? (yes/no): ");
            String response = scanner.nextLine().trim().toLowerCase();
            playAgain = response.equals("yes") || response.equals("y");
        }

        // Final stats
        System.out.println("\nGame Ended!");
        System.out.println("Final Score: " + totalScore);
        System.out.println("Rounds Played: " + roundsPlayed);
        
        scanner.close();
    }

    // Calculate score based on attempts used
    private static int calculateScore(int attempts, int maxAttempts) {
        // Score is based on how few attempts were used
        return Math.max(0, (maxAttempts - attempts + 1) * 10);
    }
}