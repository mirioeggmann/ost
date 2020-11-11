import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class Module2 {
    private final String name;
    private final Set<Module2> nextModules = new HashSet<>();
    private int amountRequiredModules;

    public Module2(String name) {
        this.name = name;
    }

    public void addNextModule(Module2 module) {
        nextModules.add(module);
    }

    public String getName() {
        return name;
    }

    public Set<Module2> getNextModules() {
        return nextModules;
    }

    public int getAmountRequiredModules() {
        return amountRequiredModules;
    }

    public void setAmountRequiredModules(int amountRequiredModules) {
        this.amountRequiredModules = amountRequiredModules;
    }

    @Override
    public String toString() {
        return "Module{" +
                "name='" + name + '\'' +
                ", nextModules=" + nextModules +
                ", amountRequiredModules=" + amountRequiredModules +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Module2 module = (Module2) o;
        return Objects.equals(name, module.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
