SOURCE = Project_Group2.py
TARGET = AB

# Default Rule
all: $(TARGET)

# Rule to create the executable 'AB' from 'Project_Group2.py'
$(TARGET):
	@echo '#!/bin/bash' > $(TARGET)
	@echo 'python3 $(SOURCE) "$$@"' >> $(TARGET)
	@chmod +x $(TARGET)
	@echo "Build successful. Created wrapper script '$(TARGET)'."

# Clean rule to remove generated files
clean:
	rm -f $(TARGET)
	rm -rf __pycache__