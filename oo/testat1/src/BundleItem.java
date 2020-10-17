import java.util.ArrayList;
import java.util.List;

public class BundleItem extends Item {
    private final List<Item> items = new ArrayList<>();
    private int discount;

    public BundleItem(String description, int discount) {
        super(description);
        this.discount = discount;
    }

    @Override
    public double getPrice() {
        double totalPrice = 0.0;
        for (Item item : this.items) {
            totalPrice += item.getPrice();
        }
        return totalPrice / 100.0 * (100.0 - this.discount);
    }

    @Override
    public void print() {
        System.out.println("BundleItem - Description: " + this.getDescription() + ", Discount: " + this.discount + "%");
        System.out.println("Start of BundleItem " + this.getDescription());
        int bundleItemIndex = 1;
        for (Item item : items) {
            System.out.print(bundleItemIndex + ". ");
            item.print();
            bundleItemIndex++;
        }
        System.out.println("End of BundleItem " + this.getDescription());
    }

    public void addItem(Item item) {
        if (this.equals(item)) {
            System.out.println("Can't add item that contains myself!");
        } else if (item instanceof BundleItem) {
            if (this.isNotContainingItselfInBundleItem(this, (BundleItem) item)) {
                this.items.add(item);
            } else {
                System.out.println("Can't add bundle that contains myself!");
            }
        } else {
            this.items.add(item);
        }
    }

    public boolean isNotContainingItselfInBundleItem(BundleItem parentBundleItem, BundleItem bundleItem) {
        List<Item> bundleItems = bundleItem.getItems();
        for (Item item : bundleItems) {
            if (item instanceof BundleItem) {
                if (parentBundleItem.equals(item)) {
                    return false;
                } else {
                    return isNotContainingItselfInBundleItem(parentBundleItem, (BundleItem) item);
                }
            }
        }
        return true;
    }

    public void removeItem(Item item) {
        items.remove(item);
    }

    public List<Item> getItems() {
        return items;
    }

    public int getDiscount() {
        return discount;
    }

    public void setDiscount(int discount) {
        this.discount = discount;
    }
}
