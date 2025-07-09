import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Represents a currency with its code, name, and symbol.
 */
class Currency {
    String code;
    String name;
    String symbol;

    public Currency(String code, String name, String symbol) {
        this.code = code;
        this.name = name;
        this.symbol = symbol;
    }

    @Override
    public String toString() {
        return code + " - " + name;
    }
}

/**
 * Fetches exchange rates and performs currency conversions.
 */
class CurrencyConverterLogic {
    // API endpoint for exchange rates. Using open.er-api.com which is free and doesn't require an API key.
    private static final String API_BASE_URL = "https://open.er-api.com/v6/latest/";
    private Map<String, Double> exchangeRates = new HashMap<>(); // Stores fetched rates
    private String currentBaseCurrency = ""; // Stores the base currency for the currently fetched rates

    // Hardcoded list of common currencies for selection
    private static final Map<String, Currency> availableCurrencies = new LinkedHashMap<>();

    static {
        availableCurrencies.put("USD", new Currency("USD", "United States Dollar", "$"));
        availableCurrencies.put("EUR", new Currency("EUR", "Euro", "€"));
        availableCurrencies.put("GBP", new Currency("GBP", "British Pound", "£"));
        availableCurrencies.put("JPY", new Currency("JPY", "Japanese Yen", "¥"));
        availableCurrencies.put("CAD", new Currency("CAD", "Canadian Dollar", "C$"));
        availableCurrencies.put("AUD", new Currency("AUD", "Australian Dollar", "A$"));
        availableCurrencies.put("CHF", new Currency("CHF", "Swiss Franc", "CHF"));
        availableCurrencies.put("CNY", new Currency("CNY", "Chinese Yuan", "¥"));
        availableCurrencies.put("INR", new Currency("INR", "Indian Rupee", "₹"));
        availableCurrencies.put("NZD", new Currency("NZD", "New Zealand Dollar", "NZ$"));
        availableCurrencies.put("MXN", new Currency("MXN", "Mexican Peso", "Mex$"));
        availableCurrencies.put("SGD", new Currency("SGD", "Singapore Dollar", "S$"));
        availableCurrencies.put("HKD", new Currency("HKD", "Hong Kong Dollar", "HK$"));
        availableCurrencies.put("NOK", new Currency("NOK", "Norwegian Krone", "kr"));
        availableCurrencies.put("SEK", new Currency("SEK", "Swedish Krona", "kr"));
        availableCurrencies.put("KRW", new Currency("KRW", "South Korean Won", "₩"));
        availableCurrencies.put("BRL", new Currency("BRL", "Brazilian Real", "R$"));
        availableCurrencies.put("ZAR", new Currency("ZAR", "South African Rand", "R"));
    }

    /**
     * Fetches real-time exchange rates for a given base currency from the API.
     * This method uses HttpURLConnection for fetching data and basic string parsing for JSON.
     * @param baseCurrencyCode The 3-letter code of the base currency (e.g., "USD").
     * @return true if rates were successfully fetched, false otherwise.
     */
    public boolean fetchExchangeRates(String baseCurrencyCode) {
        if (baseCurrencyCode.equals(currentBaseCurrency) && !exchangeRates.isEmpty()) {
            System.out.println("Rates for " + baseCurrencyCode + " are already loaded.");
            return true; // Rates already loaded for this base currency
        }

        System.out.println("Fetching exchange rates for " + baseCurrencyCode + "...");
        String apiUrl = API_BASE_URL + baseCurrencyCode;
        try {
            URL url = new URL(apiUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setConnectTimeout(5000); // 5 seconds
            connection.setReadTimeout(5000);    // 5 seconds

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder content = new StringBuilder();
                while ((inputLine = in.readLine()) != null) {
                    content.append(inputLine);
                }
                in.close();
                connection.disconnect();

                // Basic JSON parsing for the "rates" object
                String jsonString = content.toString();
                // Find the "rates" object
                int ratesStartIndex = jsonString.indexOf("\"rates\":{");
                if (ratesStartIndex == -1) {
                    System.err.println("Error: 'rates' object not found in API response.");
                    return false;
                }
                int ratesEndIndex = jsonString.indexOf("}", ratesStartIndex);
                if (ratesEndIndex == -1) {
                    System.err.println("Error: Malformed 'rates' object in API response.");
                    return false;
                }
                String ratesJson = jsonString.substring(ratesStartIndex + "\"rates\":{".length(), ratesEndIndex + 1);

                // Clear previous rates and populate new ones
                exchangeRates.clear();
                Pattern pattern = Pattern.compile("\"([A-Z]{3})\":([0-9]+\\.?[0-9]*)");
                Matcher matcher = pattern.matcher(ratesJson);
                while (matcher.find()) {
                    String code = matcher.group(1);
                    double rate = Double.parseDouble(matcher.group(2));
                    exchangeRates.put(code, rate);
                }

                currentBaseCurrency = baseCurrencyCode;
                System.out.println("Exchange rates fetched successfully for " + baseCurrencyCode + ".");
                return true;
            } else {
                System.err.println("Failed to fetch exchange rates. HTTP Error Code: " + responseCode);
                return false;
            }
        } catch (Exception e) {
            System.err.println("Error fetching exchange rates: " + e.getMessage());
            return false;
        }
    }

    /**
     * Converts an amount from a base currency to a target currency.
     * @param amount The amount to convert.
     * @param baseCurrencyCode The code of the base currency.
     * @param targetCurrencyCode The code of the target currency.
     * @return The converted amount, or -1.0 if conversion fails.
     */
    public double convert(double amount, String baseCurrencyCode, String targetCurrencyCode) {
        if (amount <= 0) {
            System.out.println("Amount must be positive.");
            return -1.0;
        }
        if (baseCurrencyCode.equals(targetCurrencyCode)) {
            System.out.println("Base and target currencies cannot be the same.");
            return -1.0;
        }

        // Ensure rates are loaded for the current base currency
        if (!baseCurrencyCode.equals(currentBaseCurrency) || exchangeRates.isEmpty()) {
            if (!fetchExchangeRates(baseCurrencyCode)) {
                System.out.println("Cannot perform conversion: Failed to fetch rates for " + baseCurrencyCode);
                return -1.0;
            }
        }

        Double targetRate = exchangeRates.get(targetCurrencyCode);
        if (targetRate == null) {
            System.out.println("Exchange rate for " + targetCurrencyCode + " not found.");
            return -1.0;
        }

        // The API returns rates relative to the base, so the base rate is effectively 1.
        // Converted Amount = Amount * Target_Rate (relative to Base)
        return amount * targetRate;
    }

    /**
     * Returns the map of available currencies.
     * @return A map of currency codes to Currency objects.
     */
    public static Map<String, Currency> getAvailableCurrencies() {
        return availableCurrencies;
    }

    /**
     * Gets the symbol for a given currency code.
     * @param currencyCode The 3-letter currency code.
     * @return The currency symbol, or the code itself if symbol not found.
     */
    public static String getCurrencySymbol(String currencyCode) {
        Currency currency = availableCurrencies.get(currencyCode);
        return (currency != null) ? currency.symbol : currencyCode;
    }
}

/**
 * Main class to run the Currency Converter as a console application.
 */
public class CurrencyConverterApplication {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        CurrencyConverterLogic converter = new CurrencyConverterLogic();

        System.out.println("\nWelcome to the Java Console Currency Converter!");

        // Initial fetch of rates for a default base currency (e.g., USD)
        // This makes the first conversion faster if USD is chosen as base.
        converter.fetchExchangeRates("USD");

        boolean running = true;
        while (running) {
            displayMenu();
            int choice = getUserChoice(scanner);

            switch (choice) {
                case 1: // Convert Currency
                    performConversion(scanner, converter);
                    break;
                case 2: // List Available Currencies
                    listCurrencies();
                    break;
                case 3: // Exit
                    running = false;
                    System.out.println("Thank you for using the Currency Converter. Goodbye!");
                    break;
                default:
                    System.out.println("Invalid option. Please try again.");
                    break;
            }
            System.out.println(); // Add a newline for better readability
        }

        scanner.close();
    }

    /**
     * Displays the main menu options.
     */
    private static void displayMenu() {
        System.out.println("Currency Converter Menu:");
        System.out.println("1. Convert Currency");
        System.out.println("2. List Available Currencies");
        System.out.println("3. Exit");
        System.out.print("Choose an option: ");
    }

    /**
     * Gets a valid integer choice from the user.
     * @param scanner The Scanner object.
     * @return The user's choice, or -1 if invalid.
     */
    private static int getUserChoice(Scanner scanner) {
        try {
            return scanner.nextInt();
        } catch (InputMismatchException e) {
            System.out.println("Invalid input. Please enter a number.");
            scanner.next(); // Consume the invalid input
            return -1;
        } finally {
            scanner.nextLine(); // Consume the rest of the line after nextInt()
        }
    }

    /**
     * Gets a valid double amount from the user.
     * @param scanner The Scanner object.
     * @param prompt The message to display.
     * @return The amount, or -1.0 if invalid.
     */
    private static double getAmountInput(Scanner scanner, String prompt) {
        System.out.print(prompt);
        try {
            double amount = scanner.nextDouble();
            if (amount < 0) {
                System.out.println("Amount cannot be negative.");
                return -1.0;
            }
            return amount;
        } catch (InputMismatchException e) {
            System.out.println("Invalid input. Please enter a valid number.");
            scanner.next(); // Consume the invalid input
            return -1.0;
        } finally {
            scanner.nextLine(); // Consume the rest of the line
        }
    }

    /**
     * Prompts the user to select a currency and validates the input.
     * @param scanner The Scanner object.
     * @param prompt The message to display.
     * @return The valid 3-letter currency code, or null if invalid.
     */
    private static String getCurrencyChoice(Scanner scanner, String prompt) {
        System.out.print(prompt);
        String currencyCode = scanner.nextLine().trim().toUpperCase();
        if (CurrencyConverterLogic.getAvailableCurrencies().containsKey(currencyCode)) {
            return currencyCode;
        } else {
            System.out.println("Invalid currency code. Please choose from the list (e.g., USD, EUR).");
            return null;
        }
    }

    /**
     * Handles the currency conversion process.
     * @param scanner The Scanner object.
     * @param converter The CurrencyConverterLogic instance.
     */
    private static void performConversion(Scanner scanner, CurrencyConverterLogic converter) {
        System.out.println("\n--- Currency Conversion ---");
        listCurrencies(); // Show available currencies

        String baseCurrency = null;
        while (baseCurrency == null) {
            baseCurrency = getCurrencyChoice(scanner, "Enter base currency code (e.g., USD): ");
        }

        String targetCurrency = null;
        while (targetCurrency == null || targetCurrency.equals(baseCurrency)) {
            targetCurrency = getCurrencyChoice(scanner, "Enter target currency code (e.g., EUR): ");
            if (targetCurrency != null && targetCurrency.equals(baseCurrency)) {
                System.out.println("Base and target currencies cannot be the same. Please choose a different target currency.");
            }
        }

        double amount = -1.0;
        while (amount <= 0) {
            amount = getAmountInput(scanner, "Enter amount to convert: ");
        }

        double convertedAmount = converter.convert(amount, baseCurrency, targetCurrency);

        if (convertedAmount != -1.0) {
            String targetSymbol = CurrencyConverterLogic.getCurrencySymbol(targetCurrency);
            System.out.printf("Result: %.2f %s = %s %.2f %s%n",
                    amount, baseCurrency, targetSymbol, convertedAmount, targetCurrency);
        } else {
            System.out.println("Conversion failed. Please check your inputs and try again.");
        }
    }

    /**
     * Lists all available currencies to the console.
     */
    private static void listCurrencies() {
        System.out.println("\n--- Available Currencies ---");
        CurrencyConverterLogic.getAvailableCurrencies().forEach((code, currency) ->
                System.out.println(code + " - " + currency.name + " (" + currency.symbol + ")")
        );
        System.out.println("----------------------------");
    }
}
