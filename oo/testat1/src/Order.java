import java.util.ArrayList;
import java.util.List;

public class Order {
    private final List<Item> items = new ArrayList<>();

    public void addItem(Item item) {
        items.add(item);
    }

    public double getTotalPrice() {
        double totalPrice = 0.0;
        for (Item item : items) {
            totalPrice += item.getPrice();
        }
        return totalPrice;
    }

    public void printItems() {
        System.out.println("--- All items of the order: ----");
        for (Item item : items) {
            item.print();
        }
        System.out.println("--------------------------------");
    }
}
