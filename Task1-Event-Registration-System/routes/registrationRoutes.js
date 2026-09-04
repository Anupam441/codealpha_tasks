const express = require("express");
const router = express.Router();
const {
  registerForEvent,
  cancelRegistration,
  getMyRegistrations,
} = require("../controllers/registrationController");
const { protect } = require("../middleware/authMiddleware");

router.get("/my-events", protect, getMyRegistrations);

router.post("/:eventId", protect, registerForEvent);
router.delete("/:eventId", protect, cancelRegistration);

module.exports = router;
