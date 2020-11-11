import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class Module {
    private final String name;
    private final Set<Module> nextModules = new HashSet<>();
    private int amountRequiredModules;

    public Module(String name) {
        this.name = name;
    }

    public void addNextModule(Module module) {
        nextModules.add(module);
    }

    public String getName() {
        return name;
    }

    public Set<Module> getNextModules() {
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
        Module module = (Module) o;
        return Objects.equals(name, module.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
