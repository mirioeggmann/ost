package ch.ost.aif.dialogflow.dialogflow;

import java.io.IOException;
import java.util.Map;
import java.util.regex.Pattern;

import ch.ost.aif.portfolio.PortfolioManager;
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.dialogflow.v2.*;

import com.google.protobuf.Value;

public class CustomRequestBuilder {

	// same as template
	public static void detectIntentTexts(String projectId, String text, String sessionId, String languageCode,
										 PortfolioManager portfolioManager) throws IOException, ApiException {
		// Instantiates a client
		try (SessionsClient sessionsClient = SessionsClient.create()) {
			// Set the session name using the sessionId (UUID) and projectID (my-project-id)
			SessionName session = SessionName.of(projectId, sessionId);

			// Add email for specific intents if not already given in text
			Pattern VALID_EMAIL_ADDRESS_REGEX =
					Pattern.compile("[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}", Pattern.CASE_INSENSITIVE);
			boolean containsEmail = VALID_EMAIL_ADDRESS_REGEX.matcher(text).find();

			if (!containsEmail) {
				text = text + " " + portfolioManager.getActivePortfolio();
			}

			// Set the text (hello) and language code (en-US) for the query
			TextInput.Builder textInput = TextInput.newBuilder().setText(text).setLanguageCode(languageCode);

			// Build the query with the TextInput
			QueryInput queryInput = QueryInput.newBuilder().setText(textInput).build();

			// Performs the detect intent request
			DetectIntentResponse response = sessionsClient.detectIntent(session, queryInput);

			// Display the query result
			QueryResult queryResult = response.getQueryResult();

			// own code
			// get the intent as a String
			String intent = queryResult.getIntent().getDisplayName();

			// print the text answer
			System.out.println(queryResult.getFulfillmentText());
			// switch-case to treat different intents differently
			switch (intent) {
			case "Default Welcome Intent": // just checking that it is the welcome intent
				break;
			case "portfolio.select":
				for (Map.Entry<String, Value> entry : queryResult.getParameters().getFieldsMap().entrySet()) {
					if(entry.getKey().equals("email")) {
						portfolioManager.updateActivePortfolio(entry.getValue().getStringValue());
					}
				}
				break;
			case "portfolio.create":
				for (Map.Entry<String, Value> entry : queryResult.getParameters().getFieldsMap().entrySet()) {
					if(entry.getKey().equals("email")) {
						portfolioManager.updateActivePortfolio(entry.getValue().getStringValue());
					}
				}
				break;
			case "Goodbye":
				System.out.println("Thank you, goodbye");
				break;
			}
		}
	}
}
