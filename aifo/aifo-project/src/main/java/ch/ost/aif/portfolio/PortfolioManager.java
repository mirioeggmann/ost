package ch.ost.aif.portfolio;

public class PortfolioManager {
    private final Portfolio portfolio;

    public PortfolioManager() {
        this.portfolio = new Portfolio("");
    }

    public void updateActivePortfolio(String email) {
        portfolio.setEmail(email);
    }

    public String getActivePortfolio() {
        return portfolio.getEmail();
    }
}
