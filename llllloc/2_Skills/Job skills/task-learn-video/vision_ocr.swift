// vision_ocr.swift - read the text on a picture with Apple's own text reader (Vision), no install needed.
// Build once:  swiftc -O vision_ocr.swift -o vision_ocr        (study_video.py does this on first run)
// Run:         ./vision_ocr <image.png> [words.txt]            words.txt = one app word per line (node and setting names)
// Prints one JSON object per line: {"text": "...", "conf": 0.93, "box": [x, y, w, h]}  box in 0..1, origin bottom-left (Vision's way).
// Language correction is OFF so node names and numbers come back as drawn, not "corrected" into English words.
import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2, let img = NSImage(contentsOfFile: args[1]), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    FileHandle.standardError.write("usage: vision_ocr <image> [words.txt]  (image not readable)\n".data(using: .utf8)!); exit(2)
}
let req = VNRecognizeTextRequest { r, e in
    guard let obs = r.results as? [VNRecognizedTextObservation] else { return }
    for o in obs {
        guard let c = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        let t = c.string.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"")
        print("{\"text\": \"\(t)\", \"conf\": \(String(format: "%.2f", c.confidence)), \"box\": [\(String(format: "%.3f", b.minX)), \(String(format: "%.3f", b.minY)), \(String(format: "%.3f", b.width)), \(String(format: "%.3f", b.height))]}")
    }
}
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
req.recognitionLanguages = ["en-US"]
if args.count >= 3, let words = try? String(contentsOfFile: args[2], encoding: .utf8) {
    req.customWords = words.split(separator: "\n").map { String($0).trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty }
}
try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
