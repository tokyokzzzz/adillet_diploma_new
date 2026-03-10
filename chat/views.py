from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404, JsonResponse
from django.db.models import Q
from profiles.models import MentorProfile
from .models import Conversation, Message
from .forms import MessageForm


@login_required
@require_POST
def start_chat(request, mentor_pk):
    """Applicant sends a chat request to a mentor (POST only)."""
    if not request.user.is_applicant():
        raise Http404

    mentor_profile = get_object_or_404(MentorProfile, pk=mentor_pk)
    conversation, created = Conversation.objects.get_or_create(
        applicant=request.user,
        mentor=mentor_profile.user,
        defaults={"status": Conversation.STATUS_PENDING},
    )
    return redirect("conversation_detail", pk=conversation.pk)


@login_required
@require_POST
def accept_chat(request, pk):
    """Mentor accepts a pending chat request."""
    conversation = get_object_or_404(Conversation, pk=pk, mentor=request.user)
    if conversation.is_pending():
        conversation.status = Conversation.STATUS_ACTIVE
        conversation.save()
    return redirect("conversation_detail", pk=pk)


@login_required
@require_POST
def decline_chat(request, pk):
    """Mentor declines a pending chat request."""
    conversation = get_object_or_404(Conversation, pk=pk, mentor=request.user)
    if conversation.is_pending():
        conversation.status = Conversation.STATUS_DECLINED
        conversation.save()
    return redirect("conversation_list")


@login_required
def conversation_list(request):
    all_convs = (
        Conversation.objects
        .filter(Q(applicant=request.user) | Q(mentor=request.user))
        .select_related("applicant", "mentor")
    )

    pending = []
    active = []
    declined = []

    for conv in all_convs:
        conv.last_message = conv.messages.last()
        if conv.is_pending():
            pending.append(conv)
        elif conv.is_active():
            active.append(conv)
        else:
            declined.append(conv)

    return render(request, "chat/conversation_list.html", {
        "pending": pending,
        "active": active,
        "declined": declined,
    })


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.user not in (conversation.applicant, conversation.mentor):
        raise Http404

    chat_messages = conversation.messages.select_related("sender")
    last_msg = chat_messages.last()
    other = conversation.other_participant(request.user)

    return render(request, "chat/conversation_detail.html", {
        "conversation": conversation,
        "chat_messages": chat_messages,
        "last_message_id": last_msg.pk if last_msg else 0,
        "other": other,
    })


@login_required
@require_POST
def send_message(request, pk):
    """AJAX: send a message, return the new message as JSON."""
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.user not in (conversation.applicant, conversation.mentor):
        raise Http404

    if not conversation.is_active():
        return JsonResponse({"error": "Conversation is not active."}, status=400)

    text = request.POST.get("text", "").strip()
    if not text:
        return JsonResponse({"error": "Message cannot be empty."}, status=400)

    msg = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        text=text,
    )
    conversation.save()

    return JsonResponse({
        "id": msg.pk,
        "text": msg.text,
        "sender_role": msg.sender.role,
        "timestamp": msg.timestamp.strftime("%b %-d, %H:%M"),
    })


@login_required
def poll_messages(request, pk):
    """AJAX: return all messages newer than ?after=<id>."""
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.user not in (conversation.applicant, conversation.mentor):
        raise Http404

    after_id = int(request.GET.get("after", 0))
    new_msgs = (
        conversation.messages
        .filter(pk__gt=after_id)
        .select_related("sender")
    )

    data = [
        {
            "id": msg.pk,
            "text": msg.text,
            "sender_username": msg.sender.username,
            "sender_role": msg.sender.role,
            "is_mine": msg.sender == request.user,
            "timestamp": msg.timestamp.strftime("%b %-d, %H:%M"),
        }
        for msg in new_msgs
    ]

    return JsonResponse({"messages": data})
