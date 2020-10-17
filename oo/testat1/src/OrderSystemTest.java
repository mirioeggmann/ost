public class OrderSystemTest {
    public static void main(String[] args) {
        // Initialize items of student bundle (including a bundle in a bundle)
        ProductItem surfaceBookProductItem = new ProductItem("Surface Book", 5, 2000.0);
        ProductItem mouseProductItem = new ProductItem("Mouse", 5, 20.0);
        ProductItem keyboardProductItem = new ProductItem("Keyboard", 1, 50.0);
        ServiceItem setupServiceItem = new ServiceItem("Setup", 100.0);
        BundleItem officeBundleItem = new BundleItem("Utilities for the Office bundle", 10);
        officeBundleItem.addItem(mouseProductItem);
        officeBundleItem.addItem(keyboardProductItem);
        BundleItem studentBundleItem = new BundleItem("Surface Book Student Bundle", 20);
        studentBundleItem.addItem(surfaceBookProductItem);
        studentBundleItem.addItem(officeBundleItem);
        studentBundleItem.addItem(setupServiceItem);

        // Initialize other items for the order
        ProductItem monitorProductItem = new ProductItem("Monitor", 1, 1000.0);
        ServiceItem supportServiceItem = new ServiceItem("Support", 200.0);

        // Initialize the order and add items
        Order order = new Order();
        order.addItem(studentBundleItem);
        order.addItem(monitorProductItem);
        order.addItem(supportServiceItem);

        System.out.println("Main output of a happy case:");
        System.out.println("-----------------------------------------------------------------------------------------");
        order.printItems();
        System.out.println("Total price of the order: " + order.getTotalPrice());
        System.out.println();

        System.out.println("Testing if cycles in bundles are prevented:");
        System.out.println("-----------------------------------------------------------------------------------------");
        // Test if itelf can be added to the bundle items
        studentBundleItem.addItem(studentBundleItem);
        // Test if bundle can be added that contains itself in the bundle items (+test if recursive check works)
        BundleItem dangerousBundleItemLayerOne = new BundleItem("Dangerous BundleItem Layer One", 100);
        BundleItem dangerousBundleItemLayerTwo = new BundleItem("Dangerous BundleItem Layer Two", 100);
        dangerousBundleItemLayerTwo.addItem(studentBundleItem);
        dangerousBundleItemLayerOne.addItem(dangerousBundleItemLayerTwo);
        studentBundleItem.addItem(dangerousBundleItemLayerOne);
        System.out.println();

        System.out.println("Testing other requirements:");
        System.out.println("-----------------------------------------------------------------------------------------");
        changeProductItemAmount(surfaceBookProductItem, 1);
        System.out.println();
        changeProductItemPricePerUnit(surfaceBookProductItem, 3000.0);
        System.out.println();
        changeServiceItemPrice(setupServiceItem, 1000.0);
        System.out.println();
        changeBundleItemDiscount(studentBundleItem, 5);
        System.out.println();
        removeItemOfBundle(studentBundleItem, surfaceBookProductItem);
    }

    private static void changeProductItemAmount(ProductItem productItem, int newAmount) {
        System.out.println("Changing ProductItem amount to " + newAmount + "...");
        System.out.println("Current amount of " + productItem.getDescription() + ": " + productItem.getAmount());
        productItem.setAmount(newAmount);
        System.out.println("New amount of " + productItem.getDescription() + ": " + productItem.getAmount());
    }

    private static void changeProductItemPricePerUnit(ProductItem productItem, double newPricePerUnit) {
        System.out.println("Changing ProductItem price per unit to " + newPricePerUnit + "...");
        System.out.println("Current price per unit of " + productItem.getDescription()
                + ": " + productItem.getPricePerUnit());
        productItem.setPricePerUnit(newPricePerUnit);
        System.out.println("New price per unit of " + productItem.getDescription()
                + ": " + productItem.getPricePerUnit());
    }

    private static void changeServiceItemPrice(ServiceItem serviceItem, double newPrice) {
        System.out.println("Changing ServiceItem price to " + newPrice + "...");
        System.out.println("Current price of " + serviceItem.getDescription() + ": " + serviceItem.getPrice());
        serviceItem.setPrice(newPrice);
        System.out.println("New price of " + serviceItem.getDescription() + ": " + serviceItem.getPrice());
    }

    private static void changeBundleItemDiscount(BundleItem bundleItem, int newDiscount) {
        System.out.println("Changing BundleItem discount to " + newDiscount + "%...");
        System.out.println("Current discount of " + bundleItem.getDescription() + ": "
                + bundleItem.getDiscount() + "%");
        bundleItem.setDiscount(newDiscount);
        System.out.println("New discount of " + bundleItem.getDescription() + ": "
                + bundleItem.getDiscount() + "%");
    }

    private static void removeItemOfBundle(BundleItem bundleItem, Item item) {
        System.out.println("Removing BundleItem item " + item.getDescription() + "...");
        System.out.println("Current amount of bundle items from bundle " + bundleItem.getDescription()
                + ": " + bundleItem.getItems().size());
        bundleItem.removeItem(item);
        System.out.println("New amount of bundle items from bundle "
                + bundleItem.getDescription() + ": " + bundleItem.getItems().size());
    }
}
