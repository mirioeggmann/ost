import java.io.IOException;
import java.util.*;

public class StudyPlan2 {
    private final String fileName;
    private final Map<String, Module2> modules;
    private final Map<Integer, Semester2> semesters;

    public StudyPlan2(String fileName) {
        this.fileName = fileName;
        modules = new HashMap<>();
        semesters = new HashMap<>();
    }

    public void initModules() throws IOException {
        try (var reader = new CatalogueReader(fileName)) {
            String[] names;
            while ((names = reader.readNextLine()) != null) {
                if (!modules.containsKey(names[0])) {
                    modules.put(names[0], new Module2(names[0]));
                }
                var requiredModules = new HashSet<>(Arrays.asList(names).subList(1, names.length));
                for (String requiredModule : requiredModules) {
                    if (!modules.containsKey(requiredModule)) {
                        modules.put(requiredModule, new Module2(requiredModule));
                    }
                    modules.get(requiredModule).addNextModule(modules.get(names[0]));
                    modules.get(names[0]).setAmountRequiredModules(modules.get(names[0]).getAmountRequiredModules() + 1);
                }
            }
        }
    }

    public void calculateStudyPlan() throws CycleDependencyException {
        var addedModules = new HashSet<Module2>();
        int currentSemester = 1;
        while (addedModules.size() != modules.size()) {
            var semester = new Semester2(currentSemester);
            var tmpExcludedModules = new ArrayList<String>();
            var cycle = true;
            for (Module2 module : modules.values()) {
                if (module.getAmountRequiredModules() == 0 &&
                        !addedModules.contains(module) &&
                        !tmpExcludedModules.contains(module.getName())) {
                    cycle = false;
                    addedModules.add(module);
                    semester.getModules().add(module);
                    for (Module2 nextModule : module.getNextModules()) {
                        nextModule.setAmountRequiredModules(nextModule.getAmountRequiredModules() - 1);
                        tmpExcludedModules.add(nextModule.getName());
                    }
                }
            }
            if (cycle) {
                throw new CycleDependencyException("Cycle detected!");
            }
            semesters.put(currentSemester, semester);
            currentSemester++;
        }
    }

    public void printStudyPlan() {
        if (semesters.size() == 0) {
            System.out.println("Please make sure that you have a valid study cataloge before printing the study plan!");
        } else {
            for (Semester2 semester : semesters.values()) {
                System.out.print("Semester " + semester.getNumber() + ":");
                for (Module2 module : semester.getModules()) {
                    System.out.print(" " + module.getName());
                }
                System.out.println();
            }
        }
    }
}
