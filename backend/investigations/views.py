from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvestigationForm, FixAttemptForm
from .models import Investigation, FixAttempt
from django.contrib import messages
from django.views.decorators.http import require_POST
from functools import wraps
from django.http import HttpResponseForbidden


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                return HttpResponseForbidden(
                    "You don't have permission to access this page."
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def create_investigation(request):

    if request.method == "POST":
        form = InvestigationForm(request.POST)

        if form.is_valid():
            investigation = form.save(commit=False)
            investigation.created_by = request.user
            investigation.save()

            return redirect("investigation_list")

    else:
        form = InvestigationForm()

    return render(
        request,
        "investigations/create.html",
        {"form": form}
    )


@login_required
def investigation_list(request):
    investigations = Investigation.objects.all().order_by("-created_at")

    return render(
        request,
        "investigations/list.html",
        {"investigations": investigations}
    )

@login_required
def investigation_detail(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)

    # attempts = investigation.fix_attempts.all().order_by("-created_at")
    fix_attempts = FixAttempt.objects.filter(investigation=investigation).order_by("created_at")

    # print("Investigation ID:", investigation.id)
    # print("Attempts found:", attempts.count())


    return render(request,"investigations/detail.html",{"investigation": investigation, "fix_attempts": fix_attempts})

@login_required
def edit_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)

    if request.method == "POST":
        form = InvestigationForm(request.POST, instance=investigation)

        if form.is_valid():
            form.save()
            return redirect("investigation_detail", pk=investigation.pk)

    else:
        form = InvestigationForm(instance=investigation)

    return render(request,"investigations/edit.html",
        {"form": form, "investigation": investigation}
    )


@login_required
@role_required("MANAGER")
@require_POST
def reopen_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)

    if investigation.status in [
        Investigation.Status.RESOLVED,
        Investigation.Status.CLOSED
    ]:
        investigation.status = Investigation.Status.IN_PROGRESS
        investigation.save(update_fields=["status"])

        messages.success(
            request,
            "Investigation reopened successfully. You can now add new attempts."
        )

    return redirect("investigation_detail", pk=investigation.pk)

@login_required
@role_required("MANAGER")
@require_POST
def close_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)

    if investigation.status == Investigation.Status.RESOLVED:
        investigation.status = Investigation.Status.CLOSED
        investigation.save(update_fields=["status"])

        messages.success(
            request,
            "Investigation closed successfully."
        )
    else:
        messages.error(
            request,
            "Only resolved investigations can be closed."
        )

    return redirect("investigation_detail", pk=investigation.pk)


@login_required
def create_fix_attempt(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)

    if investigation.status == Investigation.Status.RESOLVED:
        messages.error(request,"This investigation is resolved. Reopen it before adding new attempts.")

        return redirect("investigation_detail", pk=investigation.pk)

    if request.method == "POST":
        form = FixAttemptForm(request.POST)

        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.investigation = investigation
            attempt.save()

            if attempt.result == FixAttempt.Result.SUCCESS:
                investigation.status = Investigation.Status.RESOLVED
                investigation.save(update_fields=["status"])

            return redirect("investigation_detail", pk=investigation.pk)

    else:
        form = FixAttemptForm()

    return render(
        request,
        "investigations/create_attempt.html",
        {
            "form": form,
            "investigation": investigation
        }
    )

