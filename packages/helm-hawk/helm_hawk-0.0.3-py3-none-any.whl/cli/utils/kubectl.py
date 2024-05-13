import subprocess



class Kubectl():
    def __init__(self,namespace,context)->None:
        self.context=context
        self.namespace = namespace
    
    def get_current_namespace(self):
        if not self.namespace:
            get_ns_command=['kubectl','config','view','--minify','-o',"jsonpath='{..namespace}'"]
            output=subprocess.check_output(get_ns_command)
            return output.decode('utf-8').strip("''")

        return self.namespace
        
    def get_current_kubecontext(self):
        if not  self.context:
            command=["kubectl",'config','current-context']
            context=subprocess.Popen(command,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
            return context
        
        return self.context


    def diff(self,template):
        try:
            namespace=self.get_current_namespace()
            context=self.get_current_kubecontext()
            kubectl_diff_command = ['kubectl', 'diff', '-n',namespace,'--context',context,'-f', '-']
            op=subprocess.run(kubectl_diff_command, input=template, text=True, capture_output=True)
            if op.returncode==1 or op.returncode==0:
                return  op.stdout
            else:
                return Exception(op.stderr)
        except subprocess.CalledProcessError as e:
            print("Error output:", e.stderr)
        