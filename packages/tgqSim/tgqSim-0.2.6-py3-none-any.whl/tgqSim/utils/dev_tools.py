from subprocess import Popen, PIPE

def get_cuda_version():
    try:
        # Run nvcc command to get CUDA version
        p = Popen(["nvcc", "--version"], stdout=PIPE)
        stdout, _ = p.communicate()
        # Extract CUDA version from the output
        output = stdout.decode('utf-8')
        output_lines = output.split("\n")
        for line in output_lines:
            if line.strip().startswith("Cuda compilation tools"):
                cuda_version = line.split()[4].rstrip(",")
                return cuda_version
        return None
    except Exception as e:
        print("Error:", e)
        return None