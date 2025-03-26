"""
JVM Setup for Tabula-py

This small module helps configure the JVM path for tabula-py.
"""

import os
import logging
import platform


def setup_jvm():
    """
    Configure the JVM path for tabula-py based on the operating system.
    This should be called before importing tabula.
    """
    system = platform.system().lower()

    try:
        if system == 'darwin':  # macOS
            os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home"
        elif system == 'linux':
            # Try common Linux Java locations
            potential_paths = [
                "/usr/lib/jvm/default-java",
                "/usr/lib/jvm/java-8-openjdk-amd64",
                "/usr/lib/jvm/java-11-openjdk-amd64"
            ]

            for path in potential_paths:
                if os.path.exists(path):
                    os.environ["JAVA_HOME"] = path
                    break
        elif system == 'windows':
            # Try to find Java in Program Files
            java_path = "C:/Program Files/Java"
            if os.path.exists(java_path):
                jdk_dirs = [d for d in os.listdir(java_path) if d.startswith("jdk")]
                if jdk_dirs:
                    # Use the first JDK found
                    os.environ["JAVA_HOME"] = os.path.join(java_path, jdk_dirs[0])

        logging.info(f"Set JAVA_HOME to {os.environ.get('JAVA_HOME', 'Not found')}")
    except Exception as e:
        logging.error(f"Error setting up JVM: {e}")
