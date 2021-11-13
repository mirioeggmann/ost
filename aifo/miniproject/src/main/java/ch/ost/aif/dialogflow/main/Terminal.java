package ch.ost.aif.dialogflow.main;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import ch.ost.aif.dialogflow.dialogflow.CustomRequestBuilder;
import ch.ost.aif.portfolio.PortfolioManager;

public class Terminal {
	public static void main(String[] args) {
		PortfolioManager portfolioManager = new PortfolioManager();
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		try {
			System.out.println("Hello, please enter a line for the client and confirm with enter, q for quit.");
			String line = "";
			while (true) {
				line = br.readLine();
				if (line.equals("")) { //skip empty lines
					continue;
				}
				if (line.equals("q")) { // quit the application
					break;
				}
				CustomRequestBuilder.detectIntentTexts("juno-converter-lqcr", line, "juno-client-1234", "en-US", portfolioManager);
			}
			System.out.println("Goodbye");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
