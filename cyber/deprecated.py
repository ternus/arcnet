
class UnpackForm(forms.Form):
    code = forms.CharField(max_length=5)

@login_required
def unpack(request, code=None):
    cp = None
    if request.method == 'POST':
        form = UnpackForm(request.POST)
        if form.is_valid():
            cp = get_object_or_404(CyberPackage, code=form.cleaned_data['code'])
    elif code:
        cp = get_object_or_404(CyberPackage, code=code)
    if cp:
        if cp.contains_trance():
            return render_to_response('contents.html', {'trance':cp.contents}, context_instance=RequestContext(request))
        else:
            p = cp.contents.cyberprogram
            bn = p.bname
            return render_to_response('contents.html', {'cp':cp,'p':p,'already_has':request.user.has_program(cp.contents)}, context_instance=RequestContext(request))
    else:
        form = UnpackForm()
        return render_to_response('unpack.html', {'form':form}, context_instance=RequestContext(request))

def integrate(request, bname, magic_key=None):
    p = get_object_or_404(CyberProgram, bname=bname)        
    if not p.verify_key(magic_key):
        messages.error(request, "Error: Invalid magic cookie!  Integration aborted.")
        return HttpResponseRedirect("/net/unpack")
    if request.user.has_program(p):
        messages.error(request, "You've already integrated that program!")
        return HttpResponseRedirect("/net/programs")
    request.user.programs.add(p) # Do the add.
    messages.success(request, "Program " + p.name + " successfully integrated.")                     
    return HttpResponseRedirect("/net/programs")
