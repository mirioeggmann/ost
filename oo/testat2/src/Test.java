import java.io.IOException;

public class Test {
    public static void main(String[] args) {
        var studyPlan = new StudyPlan("LargeCatalogue.txt");
        try {
            studyPlan.initModules();
        } catch (IOException e) {
            System.out.println("Could not read the StudyCatalogue.txt from the file system!");
        }
        try {
            long start = System.currentTimeMillis();
            studyPlan.calculateStudyPlan();
            System.out.println("calculating the study plan took: " + (System.currentTimeMillis() - start) + "ms");
        } catch (CycleDependencyException e) {
            System.out.println("No calculations possible: " + e.getMessage());
        }
        studyPlan.printStudyPlan();
    }
}
