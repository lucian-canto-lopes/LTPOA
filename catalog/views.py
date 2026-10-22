from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SampleForm
from .models import Sample


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "catalog/home.html")


@login_required
def dashboard(request):
    samples = Sample.objects.all()
    context = {
        "total": samples.count(),
        "received": samples.filter(status=Sample.Status.RECEIVED).count(),
        "analyzing": samples.filter(status=Sample.Status.ANALYZING).count(),
        "completed": samples.filter(status=Sample.Status.COMPLETED).count(),
        "recent_samples": samples[:5],
    }
    return render(request, "catalog/dashboard.html", context)


@login_required
def sample_list(request):
    samples = Sample.objects.select_related("created_by")
    query = request.GET.get("q", "").strip()
    sample_type = request.GET.get("tipo", "")
    status = request.GET.get("status", "")

    if query:
        samples = samples.filter(
            Q(code__icontains=query)
            | Q(origin__icontains=query)
            | Q(requester__icontains=query)
        )
    if sample_type:
        samples = samples.filter(sample_type=sample_type)
    if status:
        samples = samples.filter(status=status)

    return render(
        request,
        "catalog/sample_list.html",
        {
            "samples": samples,
            "query": query,
            "selected_type": sample_type,
            "selected_status": status,
            "sample_types": Sample.SampleType.choices,
            "statuses": Sample.Status.choices,
        },
    )


@login_required
def sample_create(request):
    form = SampleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        sample = form.save(commit=False)
        sample.created_by = request.user
        sample.save()
        messages.success(request, f"Amostra {sample.code} cadastrada com sucesso.")
        return redirect(sample)
    return render(request, "catalog/sample_form.html", {"form": form, "title": "Nova amostra"})


@login_required
def sample_detail(request, pk):
    sample = get_object_or_404(Sample.objects.select_related("created_by"), pk=pk)
    return render(request, "catalog/sample_detail.html", {"sample": sample})


@login_required
def sample_update(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    form = SampleForm(request.POST or None, instance=sample)
    if request.method == "POST" and form.is_valid():
        sample = form.save()
        messages.success(request, f"Amostra {sample.code} atualizada.")
        return redirect(sample)
    return render(
        request,
        "catalog/sample_form.html",
        {"form": form, "title": f"Editar {sample.code}", "sample": sample},
    )
