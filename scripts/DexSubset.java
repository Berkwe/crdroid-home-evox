import java.io.File;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

public class DexSubset {
  public static void main(String[] args) throws Exception {
    var container = DexFileFactory.loadDexContainer(new File(args[0]), Opcodes.forApi(35));
    var pool = new DexPool(Opcodes.forDexVersion(39));
    var refs = new TreeSet<String>();
    int count = 0;
    for (String entry : container.getDexEntryNames()) {
      for (ClassDef cls : container.getEntry(entry).getDexFile().getClasses()) {
        boolean selected = cls.getType().startsWith(args[2]);
        if (selected) {
          pool.internClass(cls);
          System.out.println("CLASS " + entry + " " + cls.getType());
          count++;
        }
        for (Method m : cls.getMethods()) {
          if (m.getImplementation() == null) continue;
          for (Instruction ins : m.getImplementation().getInstructions()) {
            if (ins instanceof ReferenceInstruction ri) {
              Reference ref = ri.getReference();
              String owner = ref instanceof MethodReference mr ? mr.getDefiningClass() :
                  ref instanceof FieldReference fr ? fr.getDefiningClass() :
                  ref instanceof TypeReference tr ? tr.getType() : "";
              if (selected || owner.contains("/crdroid/") || owner.contains("/ThemeEngine")) {
                if (!owner.isEmpty()) refs.add(cls.getType() + " -> " + ref);
              }
            }
          }
        }
      }
    }
    refs.forEach(s -> System.out.println("REF " + s));
    if (count > 0) {
      var output = new com.android.tools.smali.dexlib2.writer.io.FileDataStore(new File(args[1]));
      pool.writeTo(output);
      output.close();
    }
    System.out.println("SELECTED " + count);
  }
}
