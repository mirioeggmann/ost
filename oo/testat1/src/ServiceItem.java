public class ServiceItem extends Item {

    private double price;

    public ServiceItem(String description, double price) {
        super(description);
        this.price = price;
    }

    @Override
    public double getPrice() {
        return this.price;
    }

    @Override
    public void print() {
        System.out.println("ServiceItem - Description: " + this.getDescription() + ", Price: " + this.price);
    }

    public void setPrice(double price) {
        this.price = price;
    }
}
