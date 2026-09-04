const Event = require("../models/Event");
const Registration = require("../models/Registration");

const createEvent = async (req, res, next) => {
  try {
    const { title, description, date, location, capacity } = req.body;

    if (!title || !description || !date || !location || !capacity) {
      return res.status(400).json({
        success: false,
        message: "Please provide title, description, date, location and capacity",
      });
    }

    const event = await Event.create({
      title,
      description,
      date,
      location,
      capacity,
      createdBy: req.user._id,
    });

    res.status(201).json({
      success: true,
      message: "Event created successfully",
      data: event,
    });
  } catch (error) {
    next(error);
  }
};

const getEvents = async (req, res, next) => {
  try {
    const events = await Event.find()
      .populate("createdBy", "name email")
      .sort({ date: 1 });

    res.status(200).json({
      success: true,
      count: events.length,
      data: events,
    });
  } catch (error) {
    next(error);
  }
};

const getEventById = async (req, res, next) => {
  try {
    const event = await Event.findById(req.params.id).populate(
      "createdBy",
      "name email"
    );

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    const registeredCount = await Registration.countDocuments({
      event: event._id,
    });
    const availableSeats = event.capacity - registeredCount;

    res.status(200).json({
      success: true,
      data: {
        ...event.toObject(),
        registeredCount,
        availableSeats: availableSeats > 0 ? availableSeats : 0,
      },
    });
  } catch (error) {
    next(error);
  }
};

const updateEvent = async (req, res, next) => {
  try {
    const event = await Event.findById(req.params.id);

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    const isOwner = event.createdBy.toString() === req.user._id.toString();
    const isAdminUser = req.user.role === "admin";

    if (!isOwner && !isAdminUser) {
      return res.status(403).json({
        success: false,
        message: "Not authorized to update this event",
      });
    }

    const { title, description, date, location, capacity } = req.body;

    if (title) event.title = title;
    if (description) event.description = description;
    if (date) event.date = date;
    if (location) event.location = location;
    if (capacity) event.capacity = capacity;

    const updatedEvent = await event.save();

    res.status(200).json({
      success: true,
      message: "Event updated successfully",
      data: updatedEvent,
    });
  } catch (error) {
    next(error);
  }
};

const deleteEvent = async (req, res, next) => {
  try {
    const event = await Event.findById(req.params.id);

    if (!event) {
      return res.status(404).json({
        success: false,
        message: "Event not found",
      });
    }

    const isOwner = event.createdBy.toString() === req.user._id.toString();
    const isAdminUser = req.user.role === "admin";

    if (!isOwner && !isAdminUser) {
      return res.status(403).json({
        success: false,
        message: "Not authorized to delete this event",
      });
    }

    await Registration.deleteMany({ event: event._id });
    await event.deleteOne();

    res.status(200).json({
      success: true,
      message: "Event and its registrations deleted successfully",
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  createEvent,
  getEvents,
  getEventById,
  updateEvent,
  deleteEvent,
};