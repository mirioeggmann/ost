abstract public class Item {
    private final String description;

    public Item(String description) {
        this.description = description;
    }

    public abstract double getPrice();

    public abstract void print();

    public String getDescription() {
        return this.description;
    }
}