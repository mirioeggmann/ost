public class ProductItem extends Item {

    private int amount;
    private double pricePerUnit;

    public ProductItem(String description, int amount, double pricePerUnit) {
        super(description);
        this.amount = amount;
        this.pricePerUnit = pricePerUnit;
    }

    @Override
    public double getPrice() {
        return this.amount * this.pricePerUnit;
    }

    @Override
    public void print() {
        System.out.println("ProductItem - Description: " + this.getDescription() + ", Amount: "
                + this.amount + ", Price per unit: " + this.pricePerUnit);
    }

    public int getAmount() {
        return amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    public double getPricePerUnit() {
        return pricePerUnit;
    }

    public void setPricePerUnit(double pricePerUnit) {
        this.pricePerUnit = pricePerUnit;
    }
}
