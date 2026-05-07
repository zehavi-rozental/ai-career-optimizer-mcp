import py_compile
import sys
import os

# עדכון נתיב לקבצים בדירקטוריה ההורית
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

files = [
    'services/google_search.py',
    'services/ai_service.py',
    'app.py'
]

errors = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f"✅ {f} - OK")
    except py_compile.PyCompileError as e:
        print(f"❌ {f} - ERROR")
        print(f"   {e}")
        errors.append(f)

if not errors:
    print("\n✨ כל הקבצים תקינים!")
    sys.exit(0)
else:
    print(f"\n❌ {len(errors)} קבצים עם שגיאות")
    sys.exit(1)

