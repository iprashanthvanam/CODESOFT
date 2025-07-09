import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * Represents a user's bank account, storing the balance and handling basic transactions.
 */
class BankAccount {
    private double balance;

    /**
     * Constructs a new BankAccount with an initial balance.
     * The initial balance cannot be negative.
     * @param initialBalance The starting balance for the account.
     */
    public BankAccount(double initialBalance) {
        if (initialBalance < 0) {
            this.balance = 0; // Ensure balance is not negative
            System.out.println("Warning: Initial balance cannot be negative. Setting to 0.");
        } else {
            this.balance = initialBalance;
        }
        System.out.printf("Bank account created with initial balance: $%.2f%n", this.balance);
    }

    /**
     * Gets the current balance of the account.
     * @return The current balance.
     */
    public double getBalance() {
        return balance;
    }

    /**
     * Deposits a specified amount into the account.
     * @param amount The amount to deposit. Must be positive.
     * @return true if the deposit was successful, false otherwise.
     */
    public boolean deposit(double amount) {
        if (amount <= 0) {
            System.err.println("Deposit failed: Amount must be positive.");
            return false;
        }
        this.balance += amount;
        System.out.printf("Deposited $%.2f. New balance: $%.2f%n", amount, this.balance);
        return true;
    }

    /**
     * Withdraws a specified amount from the account.
     * @param amount The amount to withdraw. Must be positive.
     * @return true if the withdrawal was successful (sufficient funds), false otherwise.
     */
    public boolean withdraw(double amount) {
        if (amount <= 0) {
            System.err.println("Withdrawal failed: Amount must be positive.");
            return false;
        }
        if (this.balance >= amount) {
            this.balance -= amount;
            System.out.printf("Withdrew $%.2f. New balance: $%.2f%n", amount, this.balance);
            return true;
        } else {
            System.out.printf("Withdrawal failed: Insufficient balance. Current: $%.2f, Requested: $%.2f%n",
                    this.balance, amount);
            return false;
        }
    }
}

/**
 * Represents an ATM machine, interacting with a BankAccount.
 */
class ATM {
    private BankAccount bankAccount;

    /**
     * Constructs an ATM connected to a specific BankAccount.
     * @param bankAccount The BankAccount instance this ATM will operate on.
     */
    public ATM(BankAccount bankAccount) {
        if (bankAccount == null) {
            throw new IllegalArgumentException("ATM must be initialized with a valid BankAccount instance.");
        }
        this.bankAccount = bankAccount;
        System.out.println("ATM initialized and connected to bank account.");
    }

    /**
     * Performs a deposit operation through the ATM.
     * @param amount The amount to deposit.
     * @return A message indicating the success or failure of the deposit.
     */
    public String performDeposit(double amount) {
        if (bankAccount.deposit(amount)) {
            return String.format("Deposit successful! You deposited $%.2f. Your new balance is $%.2f.",
                    amount, bankAccount.getBalance());
        } else {
            return "Deposit failed. Please ensure the amount is positive.";
        }
    }

    /**
     * Performs a withdrawal operation through the ATM.
     * @param amount The amount to withdraw.
     * @return A message indicating the success or failure of the withdrawal.
     */
    public String performWithdrawal(double amount) {
        if (bankAccount.withdraw(amount)) {
            return String.format("Withdrawal successful! You withdrew $%.2f. Your new balance is $%.2f.",
                    amount, bankAccount.getBalance());
        } else {
            // bankAccount.withdraw already prints specific error for insufficient balance/negative amount
            return "Withdrawal failed. Please check your balance or enter a valid amount.";
        }
    }

    /**
     * Checks and returns the current balance of the connected account.
     * @return A message displaying the current balance.
     */
    public String checkBalance() {
        return String.format("Your current balance is: $%.2f", bankAccount.getBalance());
    }
}

/**
 * Main class to run the ATM simulation as a console application.
 */
public class ATMApplication {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        // Create a bank account with an initial balance
        BankAccount userAccount = new BankAccount(1000.00); // Starting with $1000
        // Create an ATM instance connected to the user's account
        ATM atm = new ATM(userAccount);

        System.out.println("\nWelcome to the Java Console ATM!");

        boolean running = true;
        while (running) {
            displayMenu();
            int choice = getUserChoice(scanner);

            switch (choice) {
                case 1: // Check Balance
                    System.out.println(atm.checkBalance());
                    break;
                case 2: // Deposit
                    double depositAmount = getAmountInput(scanner, "Enter amount to deposit: ");
                    if (depositAmount > 0) {
                        System.out.println(atm.performDeposit(depositAmount));
                    } else {
                        System.out.println("Invalid deposit amount. Please enter a positive number.");
                    }
                    break;
                case 3: // Withdraw
                    double withdrawAmount = getAmountInput(scanner, "Enter amount to withdraw: ");
                    if (withdrawAmount > 0) {
                        System.out.println(atm.performWithdrawal(withdrawAmount));
                    } else {
                        System.out.println("Invalid withdrawal amount. Please enter a positive number.");
                    }
                    break;
                case 4: // Exit
                    running = false;
                    System.out.println("Thank you for using the ATM. Goodbye!");
                    break;
                default:
                    System.out.println("Invalid option. Please try again.");
                    break;
            }
            System.out.println(); // Add a newline for better readability between operations
        }

        scanner.close(); // Close the scanner when done
    }

    /**
     * Displays the ATM menu options to the user.
     */
    private static void displayMenu() {
        System.out.println("ATM Menu:");
        System.out.println("1. Check Balance");
        System.out.println("2. Deposit");
        System.out.println("3. Withdraw");
        System.out.println("4. Exit");
        System.out.print("Choose an option: ");
    }

    /**
     * Reads and validates the user's menu choice.
     * @param scanner The Scanner object to read input.
     * @return The user's valid choice, or -1 if input is invalid.
     */
    private static int getUserChoice(Scanner scanner) {
        try {
            return scanner.nextInt();
        } catch (InputMismatchException e) {
            System.out.println("Invalid input. Please enter a number.");
            scanner.next(); // Consume the invalid input
            return -1;
        }
    }

    /**
     * Prompts the user for an amount and validates it.
     * @param scanner The Scanner object to read input.
     * @param prompt The message to display to the user.
     * @return The valid amount entered by the user, or -1 if input is invalid.
     */
    private static double getAmountInput(Scanner scanner, String prompt) {
        System.out.print(prompt);
        try {
            double amount = scanner.nextDouble();
            if (amount < 0) {
                System.out.println("Amount cannot be negative.");
                return -1; // Indicate invalid amount
            }
            return amount;
        } catch (InputMismatchException e) {
            System.out.println("Invalid input. Please enter a valid number.");
            scanner.next(); // Consume the invalid input
            return -1; // Indicate invalid amount
        }
    }
}
