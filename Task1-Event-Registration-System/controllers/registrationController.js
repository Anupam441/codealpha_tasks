const Registration = require("../models/Registration");
const Event = require("../models/Event");

const registerForEvent = async (req, res, next) => {
  try {
    const { eventId } = req.params;

    const event = await Event.findById(eventId);
    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    const alreadyRegistered = await Registration.findOne({
      user: req.user._id,
      event: eventId,
    });
    if (alreadyRegistered) {
      return res.status(400).json({
        success: false,
        message: "You are already registered for this event",
      });
    }

    const currentRegistrations = await Registration.countDocuments({
      event: eventId,
    });

    if (currentRegistrations >= event.capacity) {
      return res.status(400).json({
        success: false,
        message: "Event is full, registration not allowed",
      });
    }

    const registration = await Registration.create({
      user: req.user._id,
      event: eventId,
    });

    res.status(201).json({
      success: true,
      message: "Registered for event successfully",
      data: registration,
    });
  } catch (error) {
    next(error);
  }
};

const cancelRegistration = async (req, res, next) => {
  try {
    const { eventId } = req.params;

    const registration = await Registration.findOneAndDelete({
      user: req.user._id,
      event: eventId,
    });

    if (!registration) {
      return res.status(404).json({
        success: false,
        message: "Registration not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Registration cancelled successfully",
    });
  } catch (error) {
    next(error);
  }
};

const getMyRegistrations = async (req, res, next) => {
  try {
    const registrations = await Registration.find({ user: req.user._id })
      .populate({
        path: "event",
        select: "title description date location capacity",
      })
      .sort({ registeredAt: -1 });

    res.status(200).json({
      success: true,
      count: registrations.length,
      data: registrations,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = { registerForEvent, cancelRegistration, getMyRegistrations };