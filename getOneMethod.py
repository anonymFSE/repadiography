from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
from androguard.decompiler.dad import decompile
from androguard.core.analysis import analysis

def _unidiff_output(expected, actual):
    """
    Helper function. Returns a string containing the unified diff of two multiline strings.
    """

    import difflib
    expected=expected.splitlines(1)
    actual=actual.splitlines(1)

    diff=difflib.unified_diff(expected, actual)

    return ''.join(diff)

def diffMethod(dexO, dexR, classNameO, methodNameO, classNameR, methodNameR):
    vm = dvm.DalvikVMFormat(open(dexO, "r").read())
    vmx = analysis.VMAnalysis(vm)

    vmR = dvm.DalvikVMFormat(open(dexR, "r").read())
    vmxR = analysis.VMAnalysis(vmR)

    for method in vm.get_methods():
        for methodR in vmR.get_methods():
            if (method.get_class_name() == classNameO and method.get_name() == methodNameO) and (methodR.get_class_name() == classNameR and methodR.get_name() == methodNameR):
                mx = vmx.get_method(method)            
                ms = decompile.DvMethod(mx)
                ms.process()

                mxR = vmxR.get_method(methodR)
                msR = decompile.DvMethod(mxR)
                msR.process()

                text = (_unidiff_output(ms.get_source(), msR.get_source()))
                print("getOneMethod")
                return text

def getNewMethods(dexR, classNameR, methodNameR):
    vmR = dvm.DalvikVMFormat(open(dexR, "r").read())
    vmxR = analysis.VMAnalysis(vmR)

    for methodR in vmR.get_methods():
        if (methodR.get_class_name() == classNameR and methodR.get_name() == methodNameR):
            mxR = vmxR.get_method(methodR)
            msR = decompile.DvMethod(mxR)
            msR.process()

            text = msR.get_source()
            print("getNewMethod")
            return text

